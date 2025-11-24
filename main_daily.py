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

# Create directories for outputs
os.makedirs('plots_service', exist_ok=True)
os.makedirs('forecasts_service', exist_ok=True)
os.makedirs('forecasts_monthly_service', exist_ok=True)

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
        
        # Create safe filename from service name
        safe_service_name = service.replace('/', '_').replace('\\', '_').replace(' ', '_')
        
        # Save forecast plot
        fig1 = model.plot(forecast)
        fig1.savefig(f'plots_service/forecast_plot_{safe_service_name}.png', dpi=600, bbox_inches='tight')
        plt.close(fig1)
        
        # Save components plot
        fig2 = model.plot_components(forecast)
        fig2.savefig(f'plots_service/forecast_components_plot_{safe_service_name}.png', dpi=600, bbox_inches='tight')
        plt.close(fig2)
        
        # Merge forecast with original data to include real y values
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].merge(df[['ds', 'y']], on='ds', how='left')
        result = result[['ds', 'y', 'yhat', 'yhat_lower', 'yhat_upper']]
        
        result['shamsi_ds'] = result['ds'].apply(gregorian_to_shamsi)
        result['shamsi_year_month'] = result['ds'].apply(gregorian_to_shamsi_year_month)
        result['service'] = service
        result.to_csv(f"forecasts_service/forecast_{safe_service_name}.csv", index=False)
        
        # Aggregate by month
        result_aggregated_on_month = (
            result.groupby(["shamsi_year_month"], as_index=False)
              .agg(y=("y", "sum"), yhat=("yhat", "sum"), yhat_lower=("yhat_lower", "sum"), yhat_upper=("yhat_upper", "sum"))
        )
        result_aggregated_on_month['service'] = service
        result_aggregated_on_month.to_csv(f"forecasts_monthly_service/forecast_monthly_{safe_service_name}.csv", index=False)
        
        # Plot last 365 days
        last_365_days = result.tail(365)
        plt.figure(figsize=(12, 6))
        plt.plot(last_365_days['ds'], last_365_days['y'], color='blue', linewidth=1, label='Real y')
        plt.plot(last_365_days['ds'], last_365_days['yhat'], color='red', linewidth=1, label='yhat (Predicted)')
        plt.xlabel('Date (ds)')
        plt.ylabel('Value')
        plt.title(f'Forecast vs Real Values - {service}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'plots_service/last_365_days_{safe_service_name}.png', dpi=600, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Completed {service}")
        
    except Exception as e:
        print(f"  ✗ Error processing {service}: {str(e)}")
        continue

print("\n" + "="*50)
print("All services processed!")
print(f"Results saved in:")
print(f"  - forecasts/ (daily forecasts)")
print(f"  - forecasts_monthly/ (monthly aggregated)")
print(f"  - plots/ (visualizations)")