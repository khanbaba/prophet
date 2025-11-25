import pandas as pd

data_monthly = pd.read_csv('monthly_forecasts_with_category_with_min_diff.csv')

target_months = ['(1404-02)', '(1404-03)', '(1404-04)', '(1404-05)', '(1404-06)', '(1404-07)', '(1404-08)']
filtered_data = data_monthly[data_monthly['shamsi_year_month'].isin(target_months)]

# Count frequency of each min_diff_label per service
label_counts = filtered_data.groupby(['service', 'min_diff_label']).size().reset_index(name='y_lable_frequent_count')

# Get the most frequent min_diff_label for each service
most_frequent = label_counts.loc[label_counts.groupby('service')['y_lable_frequent_count'].idxmax()]

# Rename columns to match requirements
most_frequent = most_frequent.rename(columns={
    'min_diff_label': 'y_lable_frequent'
})

most_frequent.to_csv('service_month_value_counts.csv', index=False)
