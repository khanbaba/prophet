import pandas as pd
from utils import shamsi_to_gregorian, gregorian_to_shamsi_year_month

df = pd.read_excel("PredictionFile.xlsx", sheet_name="Processed-Data")

df = df[["category", "Month", "demand_start_day", "num_submitted_orders", "Year"]]

df["ds"] = df["demand_start_day"].astype(str).apply(shamsi_to_gregorian)

result = (
    df.groupby(["ds", "category", "Year", "Month"], as_index=False)
      .agg(y=("num_submitted_orders", "sum"))
)

result.to_csv("output.csv", index=False)
