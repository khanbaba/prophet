import pandas as pd

# Read both CSV files
monthly_3years = pd.read_csv('monthly_3years_forecasts.csv')
monthly_forecasts = pd.read_csv('monthly_forecasts.csv')

# Define the months to update
months_to_update = [
    '(1404-01)', '(1404-02)', '(1404-03)', '(1404-04)',
    '(1404-05)', '(1404-06)', '(1404-07)', '(1404-08)'
]

# Filter the data for the months we need to update
forecasts_1404 = monthly_forecasts[monthly_forecasts['shamsi_year_month'].isin(months_to_update)]

# Create a dictionary for quick lookup: (shamsi_year_month, service) -> y value
lookup_dict = {}
for _, row in forecasts_1404.iterrows():
    key = (row['shamsi_year_month'], row['service'])
    lookup_dict[key] = row['y']

# Update the y values in monthly_3years_forecasts
updated_count = 0
for idx, row in monthly_3years.iterrows():
    if row['shamsi_year_month'] in months_to_update:
        key = (row['shamsi_year_month'], row['service'])
        if key in lookup_dict:
            monthly_3years.at[idx, 'y'] = lookup_dict[key]
            updated_count += 1

print(f"Updated {updated_count} rows")

# Save the updated file
monthly_3years.to_csv('monthly_3years_forecasts_updated.csv', index=False)
print("File saved successfully!")

