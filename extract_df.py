import pandas as pd
from utils import shamsi_to_gregorian, gregorian_to_shamsi_year_month

df = pd.read_excel("PredictionFile.xlsx", sheet_name="Sheet1")

df = df[["service", "demand_start_day", "num_submitted_orders", "Year"]]

# df = df[df["category"] == "نظافت و پذیرایی"]

df["ds"] = df["demand_start_day"].astype(str).apply(shamsi_to_gregorian)

result = (
    df.groupby(["ds", "service", "Year"], as_index=False)
      .agg(y=("num_submitted_orders", "sum"))
)



# rest = result.groupby(["shamsi_year_month", "service"], as_index=False).agg(y=("y", "sum"))

# final = rest.groupby(["service"], as_index=False).agg(y=("y", "sum"), count=("y", "count"))

result.to_csv("output.csv", index=False)
# rest.to_csv("output_aggregated_month.csv", index=False)
# final.to_csv("output_aggregated_service.csv", index=False)
