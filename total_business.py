from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
from utils import gregorian_to_shamsi, gregorian_to_shamsi_year_month
import os
os.makedirs('plots_overall', exist_ok=True)
os.makedirs('forecasts_overall', exist_ok=True)
os.makedirs('forecasts_monthly_overall', exist_ok=True)

data = pd.read_csv('output.csv')
data['ds'] = pd.to_datetime(data['ds'])

model = Prophet()
model.fit(data)
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

fig1 = model.plot(forecast)
fig1.savefig(f'plots_overall/forecast_plot_overall.png', dpi=600, bbox_inches='tight')
plt.close(fig1)

# Save components plot
fig2 = model.plot_components(forecast)
fig2.savefig(f'plots_overall/forecast_components_plot_overall.png', dpi=600, bbox_inches='tight')
plt.close(fig2)

result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].merge(data[['ds', 'y']], on='ds', how='left')
result = result[['ds', 'y', 'yhat', 'yhat_lower', 'yhat_upper']]

result['shamsi_ds'] = result['ds'].apply(gregorian_to_shamsi)
result['shamsi_year_month'] = result['ds'].apply(gregorian_to_shamsi_year_month)
result.to_csv(f"forecasts_overall/forecast_overall.csv", index=False)

# Aggregate by month
result_aggregated_on_month = (
    result.groupby(["shamsi_year_month"], as_index=False)
        .agg(y=("y", "sum"), yhat=("yhat", "sum"), yhat_lower=("yhat_lower", "sum"), yhat_upper=("yhat_upper", "sum"))
)
result_aggregated_on_month.to_csv(f"forecasts_monthly_overall/forecast_monthly_overall.csv", index=False)

print(len(result_aggregated_on_month))
print(len(result))

# Plot last 365 days
last_365_days = result.tail(1462)
plt.figure(figsize=(12, 6))
plt.plot(last_365_days['ds'], last_365_days['y'], color='blue', linewidth=1, label='Real y')
plt.plot(last_365_days['ds'], last_365_days['yhat'], color='red', linewidth=1, label='yhat (Predicted)')
plt.xlabel('Date (ds)')
plt.ylabel('Value')
plt.title(f'Forecast vs Real Values - Overall')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'plots_overall/last_1462_days_overall.png', dpi=600, bbox_inches='tight')
plt.close()