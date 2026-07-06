import streamlit as st
from scripts.get_nyiso_load_data import (
    get_5_minute_intervals,
    get_10_minute_intervals,
    get_30_minute_intervals,
    get_1_hour_intervals,
    get_available_dates,
)
import pandas as pd
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from dotenv import load_dotenv
import datetime

load_dotenv()
schema = "NYISO_NYC_Load_Actual_5_Minute"

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
    options=ClientOptions(schema=schema)
)

st.title("NYISO Energy Load Dashboard")

interval = st.selectbox(
    "Select an interval", 
    ["5 minutes", "10 minutes", "30 minutes", "1 hour"], 
    key="select_interval"
    )
# date = st.selectbox(
#     "Select a date",
#     get_available_dates(),
#     key="select_date"
# )

dates=get_available_dates()

start = datetime.date.fromisoformat(dates[0])
end = datetime.date.fromisoformat(dates[-1])

date_interval = st.date_input(
    "Select your date interval",
    (start, start),
    start,
    end,
    format="MM.DD.YYYY",
)
# Convert date_interval back to iso format
date_interval = (
    datetime.date.isoformat(date_interval[0]),
    datetime.date.isoformat(date_interval[1])
)

st.write(f"Current interval: {interval}")
if interval == "5 minutes":
    data = get_5_minute_intervals(start=date_interval[0], end=date_interval[1])
elif interval == "10 minutes":
    data = get_10_minute_intervals(start=date_interval[0], end=date_interval[1])
elif interval == "30 minutes":
    data = get_30_minute_intervals(start=date_interval[0], end=date_interval[1])
elif interval == "1 hour":
    data = get_1_hour_intervals(start=date_interval[0], end=date_interval[1])
else:
    data=None

if data is not None:
    st.line_chart(data, x="RTD_End_Time_Stamp", y="RTD_Actual_Load", x_label="Time", y_label="Load")
else:
    st.write("No data available")