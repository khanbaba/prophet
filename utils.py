import jdatetime
from datetime import datetime
import pandas as pd

def shamsi_to_gregorian(shamsi_date_str):
    y, m, d = map(int, shamsi_date_str.split("/"))
    g = jdatetime.date(y, m, d).togregorian()
    return g.strftime("%Y-%m-%d")

def gregorian_to_shamsi(gregorian_date_str):
    # Handle both string and pandas Timestamp objects
    if isinstance(gregorian_date_str, (pd.Timestamp, datetime)):
        g = gregorian_date_str
    else:
        g = datetime.strptime(gregorian_date_str, "%Y-%m-%d")
    s = jdatetime.date.fromgregorian(date=g)
    return s.strftime("%Y/%m/%d")

def gregorian_to_shamsi_year_month(gregorian_date_str):
    # Handle both string and pandas Timestamp objects
    if isinstance(gregorian_date_str, (pd.Timestamp, datetime)):
        g = gregorian_date_str
    else:
        g = datetime.strptime(gregorian_date_str, "%Y-%m-%d")
    s = jdatetime.date.fromgregorian(date=g)
    return s.strftime("(%Y-%m)")