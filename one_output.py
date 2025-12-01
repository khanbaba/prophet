from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
from utils import gregorian_to_shamsi, gregorian_to_shamsi_year_month
import os
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt


d = pd.read_csv('output.csv')
d['ds'] = pd.to_datetime(d['ds'])

target_years = [1401, 1402, 1403]
# data = d[d['Year'].isin(target_years)]
data = d[
    (d['Year'].isin(target_years)) | 
    ((d['Year'] == 1404) & (d['Month'].isin([1, 2, 3, 4, 5, 6])))
]

# Get all unique categorys
categorys = data['category'].unique()
print(f"Found {len(categorys)} category")


res_mape = []

all_daily_forecasts = []
all_monthly_forecasts = []
for idx, category in enumerate(categorys, 1):
    print(f"\n[{idx}/{len(categorys)}] Processing category: {category}")
    
    # Filter data for this category
    df = data[data['category'] == category][['ds', 'y']].copy()
    df_with_1404 = d[d['category'] == category][['ds', 'y']].copy()
    
    try:
        model = Prophet(
            changepoint_prior_scale=0.01
        )
        model.fit(df)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)

        fig1 = model.plot(forecast)
        name = f"plots_done_0_01/{category}.png"
        fig1.savefig(name, dpi=300)
        plt.close(fig1)
        
        # Merge forecast with original data to include real y values
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].merge(df_with_1404[['ds', 'y']], on='ds', how='left')
        result = result[['ds', 'y', 'yhat', 'yhat_lower', 'yhat_upper']]
        
        result['shamsi_ds'] = result['ds'].apply(gregorian_to_shamsi)
        result['shamsi_year_month'] = result['ds'].apply(gregorian_to_shamsi_year_month)
        result['category'] = category
        
        all_daily_forecasts.append(result)
        
        result_aggregated_on_month = (
            result.groupby(["shamsi_year_month"], as_index=False)
            .agg(y=("y", "sum"), yhat=("yhat", "sum"), yhat_lower=("yhat_lower", "sum"), yhat_upper=("yhat_upper", "sum"))
        )
        result_aggregated_on_month['category'] = category
        
        all_monthly_forecasts.append(result_aggregated_on_month)
        
        
    except Exception as e:
        print(f"  ✗ Error processing {category}: {str(e)}")
        continue


# Combine all results and save to single files
if all_daily_forecasts:
    combined_daily = pd.concat(all_daily_forecasts, ignore_index=True)
    combined_daily.to_csv("daily_3years_forecasts.csv", index=False)
    print(f"\n✓ Saved daily forecasts for all categorys to: all_categorys_daily_forecasts.csv")
    print(f"  Total rows: {len(combined_daily)}")

if all_monthly_forecasts:
    combined_monthly = pd.concat(all_monthly_forecasts, ignore_index=True)
    combined_monthly.to_csv("monthly_3years_forecasts.csv", index=False)
    mape = mean_absolute_percentage_error(combined_monthly["y"], combined_monthly["yhat"]) * 100
    print(f"mape: {mape}")
    print(f"✓ Saved monthly forecasts for all categorys to: all_categorys_monthly_forecasts.csv")
    print(f"  Total rows: {len(combined_monthly)}")

print("\n" + "="*50)
print("All categorys processed successfully!")