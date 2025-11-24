import pandas as pd

# Read the data
data_monthly = pd.read_csv('all_services_monthly_forecasts_with_category_with_min_diff.csv')

print(data_monthly)

# Define the specific shamsi_year_month values to filter (note: they have parentheses)
target_months = ['(1404-02)', '(1404-03)', '(1404-04)', '(1404-05)', '(1404-06)', '(1404-07)', '(1404-08)']

# Filter the data for the specified months
filtered_data = data_monthly[data_monthly['shamsi_year_month'].isin(target_months)]

print(f"Total rows before filtering: {len(data_monthly)}")
print(f"Total rows after filtering: {len(filtered_data)}")
print("\n" + "="*80 + "\n")

# Calculate value_counts for each service
print("VALUE COUNTS FOR EACH SERVICE (for months 1404-02 to 1404-08):\n")

# Group by service and get the count
service_counts = filtered_data.groupby('service').size().sort_values(ascending=False)

print(service_counts)
print("\n" + "="*80 + "\n")

# If you want more detailed information, you can also show counts per service per month
print("DETAILED COUNTS PER SERVICE PER MONTH:\n")
service_month_counts = filtered_data.groupby(['service', 'shamsi_year_month']).size().unstack(fill_value=0)
print(service_month_counts)

# Save the results to CSV files
service_counts.to_csv('service_value_counts.csv', header=['count'])
service_month_counts.to_csv('service_month_value_counts.csv')

print("\n" + "="*80)
print("Results saved to:")
print("  - service_value_counts.csv")
print("  - service_month_value_counts.csv")

