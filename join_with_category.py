import pandas as pd

df = pd.read_excel("PredictionFile.xlsx", sheet_name="Sheet1")
data = pd.read_csv('daily_forecasts.csv')
data_monthly = pd.read_csv('monthly_forecasts.csv')

df = df[["service", "category"]].drop_duplicates()

data = data.merge(df, on='service', how='left')
data_monthly = data_monthly.merge(df, on='service', how='left')
data.to_csv('daily_forecasts_with_category.csv', index=False)
data_monthly.to_csv('monthly_forecasts_with_category.csv', index=False)