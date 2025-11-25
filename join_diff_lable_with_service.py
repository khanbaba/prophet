import pandas as pd

df = pd.read_csv('service_3years_month_value_counts.csv')
data = pd.read_csv('monthly_3years_forecasts_updated_with_min_diff.csv')

df = df[["service", "y_lable_frequent"]].drop_duplicates()

data = data.merge(df, on='service', how='left')
data.to_csv('monthly_3years_finall.csv', index=False)