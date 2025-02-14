#### Generate an authcode and then make a request to generate an accessToken (Login Flow)
import webbrowser
import os
from utils.env_check import load_and_check_env_variables  # Import the environment check function
load_and_check_env_variables()

from fyers_apiv3 import fyersModel
redirect_uri= "http://127.0.0.1:5001/fyers/callback"  ## redircet_uri you entered while creating APP.
client_id = "OIYZFKGE1L-100"                       ## Client_id here refers to APP_ID of the created app
secret_key = "2NQKRSSCK1"                          ## app_secret key which you got after creating the app 
grant_type = "authorization_code"                  ## The grant_type always has to be "authorization_code"
response_type = "code"                             ## The response_type always has to be "code"
state = "sample"
def genrateToken(appSession):
    
    # ## Make  a request to generate_authcode object this will return a login url which you need to open in your browser from where you can get the generated auth_code 
    generateTokenUrl = appSession.generate_authcode()
    print(generateTokenUrl)
    webbrowser.open(generateTokenUrl,new=1)

def generateAccessToken(appSession):
    ### After succesfull login the user can copy the generated auth_code over here and make the request to generate the accessToken 
    appSession.set_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3Mzk1MDQ2NTQsImV4cCI6MTczOTUzNDY1NCwibmJmIjoxNzM5NTA0MDU0LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJEVDAwNDY2Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiZjQ0NjAxN2VkN2VkYTBjM2M2Mzk1M2M1MTBiZTQzNmZlMDkwZDUzOGIxZGVhYWZjMjFmNTg2NTMiLCJpc0RkcGlFbmFibGVkIjoiWSIsImlzTXRmRW5hYmxlZCI6IlkiLCJub25jZSI6IiIsImFwcF9pZCI6Ik9JWVpGS0dFMUwiLCJ1dWlkIjoiMmIyNjkxN2NiZDUwNDMyMjllMzhiZjU1MGNkNWYzZTIiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.8qDXZR0lC9W3WfOGryk_Q9YMoC0tKMPepdSpuFrL3iI')
    response = appSession.generate_token()
    return response['access_token']

## There can be two cases over here you can successfully get the acccessToken over the request or you might get some error over here. so to avoid that have this in try except block
try:
    appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)
    # genrateToken(appSession) 
    access_token = generateAccessToken(appSession)
    print(access_token)
except Exception as e:
    print(e) 
