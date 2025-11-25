import pandas as pd

df = pd.read_excel("PredictionFile.xlsx", sheet_name="Daily")
data = pd.read_csv('daily_forecasts.csv')

df = df[["service", "category"]].drop_duplicates()

data = data.merge(df, on='service', how='left')

data.to_csv('daily_forecasts_with_category.csv', index=False)
