import pandas as pd

data = pd.read_csv('daily_3years_forecasts_with_category.csv')
data_monthly = pd.read_csv('monthly_3years_forecasts_with_category.csv')

# Calculate absolute difference between y and yhat
data['yhat_diff'] = abs(data['y'] - data['yhat'])
data['yhat_low_diff'] = abs(data['y'] - data['yhat_lower'])
data['yhat_high_diff'] = abs(data['y'] - data['yhat_upper'])

data_monthly['yhat_diff'] = abs(data_monthly['y'] - data_monthly['yhat'])
data_monthly['yhat_low_diff'] = abs(data_monthly['y'] - data_monthly['yhat_lower'])
data_monthly['yhat_high_diff'] = abs(data_monthly['y'] - data_monthly['yhat_upper'])

# Calculate the minimum of the absolute differences
data['min_diff_label'] = data[['yhat_diff', 'yhat_low_diff', 'yhat_high_diff']].idxmin(axis=1)
data_monthly['min_diff_label'] = data_monthly[['yhat_diff', 'yhat_low_diff', 'yhat_high_diff']].idxmin(axis=1)

data.to_csv('daily_3years_forecasts_with_category_with_min_diff.csv', index=False)
data_monthly.to_csv('monthly_3years_forecasts_with_category_with_min_diff.csv', index=False)

print(data['min_diff_label'].value_counts())
print(data_monthly['min_diff_label'].value_counts())

