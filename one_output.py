from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
from utils import gregorian_to_shamsi, gregorian_to_shamsi_year_month
import os

data = pd.read_csv('output.csv')
data['ds'] = pd.to_datetime(data['ds'])

# Get all unique services
services = data['service'].unique()
print(f"Found {len(services)} services")

# Create lists to collect all results
all_daily_forecasts = []
all_monthly_forecasts = []

# Loop over each service
for idx, service in enumerate(services, 1):
    print(f"\n[{idx}/{len(services)}] Processing service: {service}")
    
    # Filter data for this service
    df = data[data['service'] == service][['ds', 'y']].copy()
    
    # Skip if not enough data
    if len(df) < 2:
        print(f"  Skipping {service} - not enough data")
        continue
    
    try:
        # Train Prophet model
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)
        
        # Merge forecast with original data to include real y values
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].merge(df[['ds', 'y']], on='ds', how='left')
        result = result[['ds', 'y', 'yhat', 'yhat_lower', 'yhat_upper']]
        
        result['shamsi_ds'] = result['ds'].apply(gregorian_to_shamsi)
        result['shamsi_year_month'] = result['ds'].apply(gregorian_to_shamsi_year_month)
        result['service'] = service
        
        # Add to daily forecasts list
        all_daily_forecasts.append(result)
        
        # Aggregate by month
        result_aggregated_on_month = (
            result.groupby(["shamsi_year_month"], as_index=False)
              .agg(y=("y", "sum"), yhat=("yhat", "sum"), yhat_lower=("yhat_lower", "sum"), yhat_upper=("yhat_upper", "sum"))
        )
        result_aggregated_on_month['service'] = service
        
        # Add to monthly forecasts list
        all_monthly_forecasts.append(result_aggregated_on_month)
        
        print(f"  ✓ Completed {service}")
        
    except Exception as e:
        print(f"  ✗ Error processing {service}: {str(e)}")
        continue

# Combine all results and save to single files
if all_daily_forecasts:
    combined_daily = pd.concat(all_daily_forecasts, ignore_index=True)
    combined_daily.to_csv("daily_forecasts.csv", index=False)
    print(f"\n✓ Saved daily forecasts for all services to: all_services_daily_forecasts.csv")
    print(f"  Total rows: {len(combined_daily)}")

if all_monthly_forecasts:
    combined_monthly = pd.concat(all_monthly_forecasts, ignore_index=True)
    combined_monthly.to_csv("monthly_forecasts.csv", index=False)
    print(f"✓ Saved monthly forecasts for all services to: all_services_monthly_forecasts.csv")
    print(f"  Total rows: {len(combined_monthly)}")

print("\n" + "="*50)
print("All services processed successfully!")