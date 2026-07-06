import streamlit as st
from src.main import display_message
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
schema = "NYISO_NYC_Load_Actual_5_Minute"

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
    options=ClientOptions(schema=schema)
)

table = supabase.table("June_2026").select("*").execute()
data = pd.DataFrame(table.data)

st.title("Energy Dashboard")

interval = st.selectbox(
    "Select an interval", 
    ["5 minutes", "10 minutes", "30 minutes", "1 hour"], 
    key="select_interval"
    )


st.write(f"Current interval: {interval}")

st.line_chart(data, x="RTD_End_Time_Stamp", y="RTD_Actual_Load", x_label="Time", y_label="Load")