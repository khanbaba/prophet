import pandas as pd

df = pd.read_csv('service_month_value_counts.csv')
data = pd.read_csv('monthly_forecasts_with_category_with_min_diff.csv')

df = df[["service", "y_lable_frequent"]].drop_duplicates()

data = data.merge(df, on='service', how='left')
data.to_csv('monthly_forecasts_with_category_with_min_diff_with_service.csv', index=False)