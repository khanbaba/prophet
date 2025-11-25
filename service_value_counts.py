import pandas as pd

data_monthly = pd.read_csv('monthly_forecasts_with_category_with_min_diff.csv')

target_months = ['(1404-02)', '(1404-03)', '(1404-04)', '(1404-05)', '(1404-06)', '(1404-07)', '(1404-08)']
filtered_data = data_monthly[data_monthly['shamsi_year_month'].isin(target_months)]

# Count frequency of each min_diff_label per service
label_counts = filtered_data.groupby(['service', 'min_diff_label']).size().reset_index(name='count')

# Pivot to get one row per service with label counts in separate columns
pivot_table = label_counts.pivot(index='service', columns='min_diff_label', values='count').fillna(0).astype(int)

# Reset index to make service a column
pivot_table = pivot_table.reset_index()

pivot_table.to_csv('service_month_value_counts.csv', index=False)
