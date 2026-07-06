import os

import pandas as pd
from dotenv import load_dotenv
from supabase import Client, create_client
from supabase.client import ClientOptions

load_dotenv()
schema = "NYISO_NYC_Load_Actual_5_Minute"

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
    options=ClientOptions(schema=schema),
)


def _query_table(
    table_name: str = "June_2026",
    start: str | None = None,
    end: str | None = None,
):
    query = supabase.table(table_name).select("*")
    if start and end:
        try:
            end_exclusive = (pd.Timestamp(end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
            query = query.gte("RTD_End_Time_Stamp", f"{start}T00:00:00").lt(
                "RTD_End_Time_Stamp", f"{end_exclusive}T00:00:00"
            )
        except Exception as e:
            raise f"An error occured while querying the table: {table_name}. Error: {e}"
    return query.execute()


def get_available_dates() -> list[str]:
    result = supabase.rpc("get_available_dates").execute()
    return [str(row["available_date"]) for row in result.data]


def get_5_minute_intervals(
    table_name: str = "June_2026",
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame:
    table = _query_table(table_name, start, end)
    return pd.DataFrame(table.data)


def get_10_minute_intervals(
    table_name: str = "June_2026",
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame:
    table = _query_table(table_name, start, end)
    df = pd.DataFrame(table.data)
    timestamps = pd.to_datetime(df["RTD_End_Time_Stamp"])
    return df[timestamps.dt.minute % 10 == 0]


def get_30_minute_intervals(
    table_name: str = "June_2026",
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame:
    table = _query_table(table_name, start, end)
    df = pd.DataFrame(table.data)
    timestamps = pd.to_datetime(df["RTD_End_Time_Stamp"])
    return df[timestamps.dt.minute % 30 == 0]


def get_1_hour_intervals(
    table_name: str = "June_2026",
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame:
    table = _query_table(table_name, start, end)
    df = pd.DataFrame(table.data)
    timestamps = pd.to_datetime(df["RTD_End_Time_Stamp"])
    return df[timestamps.dt.minute == 0]
