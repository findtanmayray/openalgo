from fyers_apiv3 import fyersModel
import requests
import json
import pandas as pd
from datetime import datetime
import os
from utils.env_check import load_and_check_env_variables  # Import the environment check function
load_and_check_env_variables()

def get_future_contract_details(stock_symbol):
    csv_url = 'https://public.fyers.in/sym_details/NSE_FO.csv'
    df = pd.read_csv(csv_url, header=None)
    df.columns = ["ID", "SYMBOL", "Unknown1", "LOT_SIZE", "Unknown2", "Unknown3",
                  "Unknown4", "EXPIRY_DATE", "Unknown5", "TICKER", "Unknown6",
                  "Unknown7", "Unknown8", "UNDERLYING", "Unknown9", "Unknown10",
                  "Unknown11", "Unknown12", "Unknown13", "Unknown14", "Unknown15"]

    df_futures = df[(df["TICKER"].str.contains(f"NSE:{stock_symbol}", na=False)) & 
                    (df["TICKER"].str.endswith("FUT"))].copy()

    df_futures.loc[:, "EXPIRY_DATE"] = pd.to_datetime(df_futures["EXPIRY_DATE"], errors='coerce')
    df_futures = df_futures.sort_values(by="EXPIRY_DATE")
    
    if df_futures.empty:
        return None

    nearest_expiry = df_futures.iloc[0]
    return {
        "Ticker Symbol": nearest_expiry["TICKER"],
        "Lot Size": int(nearest_expiry["LOT_SIZE"]),  # Ensure it's an integer
        "Underlying Symbol": nearest_expiry["UNDERLYING"]
    }


def send_margin_request(stock_symbol, side=-1, type_=2, product_type="INTRADAY", limit_price=0.0, stop_loss=0.0):
    # Get contract details
    contract_details = get_future_contract_details(stock_symbol)
    if not contract_details:
        return f"No future contract found for {stock_symbol}"

    ticker_symbol = contract_details["Ticker Symbol"]
    lot_size = contract_details["Lot Size"]

    # API endpoint
    url = "https://api-t1.fyers.in/api/v3/multiorder/margin"
    auth_code = os.getenv('auth_code')
    # API headers
    headers = {
        "Authorization": "OIYZFKGE1L-100:"+auth_code,  # Replace with actual token
        "Content-Type": "application/json"
    }

    # JSON payload
    payload = {
        "data": [{
            "symbol": ticker_symbol,
            "qty": lot_size,
            "side": side,
            "type": type_,
            "productType": product_type,
            "limitPrice": limit_price,
            "stopLoss": stop_loss
        }]
    }

    # Make API request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Return response JSON
    return response.json()


# function to get last traded price
def get_ltp(fyers,stock_symbol):
    data = {
        "symbols":stock_symbol,
    }
    return fyers.quotes(data)
# function to place order
def place_order(fyers,stock_symbol,stop_loss,target,qty,buy_order=1, type=2, product_type="BO"):
    data =  {
        "symbol":stock_symbol,
        "qty":qty,
        "type":type,# 2 means market order
        "side":buy_order,
        "productType":product_type,
        "limitPrice":0,
        "stopPrice":0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":False,
        "stopLoss":stop_loss,
        "takeProfit":target
    }  
    print(data)
    return fyers.place_order(data)