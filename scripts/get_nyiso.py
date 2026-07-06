import pandas as pd
import json
import logging
import gridstatus

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def fetch_nyiso_data():
    nyiso = gridstatus.NYISO()
    data = nyiso.get_lmp(date="today", market="REAL_TIME_5_MIN", locations="ALL")

    five_min_pricing_data_df = nyiso.get_as_prices_real_time_5_min()
    return five_min_pricing_data_df



def main():
    logger.info("Fetching NYISO data...")
    print("Fetching NYISO data...") 
    five_min_pricing_data_df = fetch_nyiso_data()
    print(five_min_pricing_data_df)
    return

if __name__ == "__main__":
    print("Checking package versions...")
    print(f"gridstatus version: {gridstatus.__version__}")
    print("Starting NYISO data fetch...")
    try:
        main()
    except Exception as e:
        logger.error(f"Error fetching NYISO data: {e}")
        print(f"Error fetching NYISO data: {e}")
        raise e
    logger.info("NYISO data fetched successfully.")
    print("NYISO data fetched successfully.")