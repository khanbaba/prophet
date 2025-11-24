import pandas as pd
from utils import shamsi_to_gregorian, gregorian_to_shamsi_year_month

df = pd.read_excel("PredictionFile.xlsx", sheet_name="Daily")
data = pd.read_csv('all_services_monthly_forecasts.csv')

df = df[["service", "category"]].drop_duplicates()

data = data.merge(df, on='service', how='left')

data.to_csv('all_services_monthly_forecasts_with_category.csv', index=False)
