from fyers_apiv3 import fyersModel
import time
from datetime import datetime
import os
from FyersUtils import get_future_contract_details, get_ltp, place_order, send_margin_request
from utils.env_check import load_and_check_env_variables  # Import the environment check function
load_and_check_env_variables()
"""
In order to get started with Fyers API we would like you to do the following things first.
1. Checkout our API docs :   https://myapi.fyers.in/docsv3
2. Create an APP using our API dashboard :   https://myapi.fyers.in/dashboard/

Once you have created an APP you can start using the below SDK 
"""
redirect_uri= "http://127.0.0.1:5001/fyers/callback"  ## redircet_uri you entered while creating APP.
client_id = "OIYZFKGE1L-100"                       ## Client_id here refers to APP_ID of the created app
secret_key = "2NQKRSSCK1"                          ## app_secret key which you got after creating the app 
grant_type = "authorization_code"                  ## The grant_type always has to be "authorization_code"
response_type = "code"                             ## The response_type always has to be "code"
state = "sample"    
### Connect to the sessionModel object here with the required input parameters
appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)

# ## Make  a request to generate_authcode object this will return a login url which you need to open in your browser from where you can get the generated auth_code 
# generateTokenUrl = appSession.generate_authcode()

# """There are two method to get the Login url if  you are not automating the login flow
# 1. Just by printing the variable name 
# 2. There is a library named as webbrowser which will then open the url for you without the hasel of copy pasting
# both the methods are mentioned below"""
# print((generateTokenUrl))  
# webbrowser.open(generateTokenUrl,new=1)

"""
run the code firstly upto this after you generate the auth_code comment the above code and start executing the below code """
##########################################################################################################################
auth_code = os.getenv('auth_code')
 ## This will help you in debugging then and there itself like what was the error and also you would be able to see the value you got in response variable. instead of getting key_error for unsuccessfull response.



## Once you have generated accessToken now we can call multiple trading related or data related apis after that in order to do so we need to first initialize the fyerModel object with all the requried params.
"""
fyerModel object takes following values as arguments
1. accessToken : this is the one which you received from above 
2. client_id : this is basically the app_id for the particular app you logged into
"""
fyers = fyersModel.FyersModel(token=auth_code,is_async=False,client_id=client_id,log_path="")


## After this point you can call the relevant apis and get started with

####################################################################################################################
"""
1. User Apis : This includes (Profile,Funds,Holdings)
"""

# print(fyers.get_profile())  ## This will provide us with the user related data 


######################################################################################################################

"""
3. Order Placement  : This Apis helps to place order. 
There are two ways to place order 
a. single order : wherein you can fire one order at a time 
b. multi order : this is used to place a basket of order but the basket size can max be 10 symbols
c. multileg order : this is used to place a multileg order but the legs size minimum is 2 and maximum is 3
"""

## SINGLE ORDER 


# this function will first get the contract details based on input symbol and then get lot size and margin required
# for near expiry future contract
def get_margin_required(stock_symbol):
    # Get contract details
    contract_details = get_future_contract_details(stock_symbol)
    if not contract_details:
        return f"No future contract found for {stock_symbol}"
    
    ticker_symbol = contract_details["Ticker Symbol"]
    lot_size = contract_details["Lot Size"]
    underlying_symbol = contract_details["Underlying Symbol"]
    
    # Get margin required
    margin_required = send_margin_request(stock_symbol)
    return {
        "Ticker Symbol": ticker_symbol,
        "Lot Size": lot_size,
        "Underlying Symbol": underlying_symbol,
        "Margin Required": margin_required
    }
#main function
def wait_until_market_open():
    now = datetime.now()
    target_time = now.replace(hour=9, minute=15, second=0)
    
    # If it's already past 6 PM, wait until 6 PM the next day
    if now >= target_time:
        target_time = target_time.replace(day=now.day + 1)
    
    wait_seconds = (target_time - now).total_seconds()
    
    print(f"Waiting for {int(wait_seconds)} seconds until market open...")
    time.sleep(wait_seconds)  # Block execution until 6 PM

    print("It's 9.15 AM! Continuing execution.")
if __name__ == "__main__":
    
    # print(stock_symbol)
    ip_stock_symbol = input("Enter the stock symbol (e.g., RELIANCE): ").strip().upper()
    ip_buy_sell = input("Enter B for buy or S for sell").strip().upper()
    stock_symbol = get_margin_required(ip_stock_symbol)  # Example input
    print(stock_symbol)
    script = stock_symbol['Ticker Symbol']
    max_lot = int(stock_symbol['Margin Required']['data']['margin_avail']/stock_symbol['Margin Required']['data']['margin_new_order'])
    buy_or_sell = 1 if ip_buy_sell == 'B' else -1
    print(f"Max lot can be taken: {max_lot}")
    ip_lot = input("Enter lot").strip()
    ip_sl = input("Enter stop loss in percentage").strip()
    ip_target = input("Enter target in percentage").strip()
    
    ip_confirmation = input("Do you want to proceed (Y/N)?").strip().upper()
    
    wait_until_market_open()
    time.sleep(10/1000)
    lp = get_ltp(fyers,script)
    print(lp)
    ltp = lp.get('d', [{}])[0].get('v', {}).get('lp')
    # sl to round off to 2 decimal places, which is divisible by 0.05
    sl = int(ltp * float(ip_sl)/100)
    target = int(ltp * float(ip_target)/100)
    print(ltp)
    print(sl)
    print(target)
    qty = int(ip_lot)*int(stock_symbol['Lot Size'])
    print(qty)
    print(place_order(fyers, script, sl, target,qty))

import time
from datetime import datetime


