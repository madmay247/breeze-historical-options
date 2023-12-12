from datetime import datetime
from breeze_connect import BreezeConnect
from BreezeHistoricalOptions import autologin, Breezy
import json, yaml, time
unix_start = time.time()

###################################################################
###################### LOGIN STUFF ################################
with open('cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    
breeze = BreezeConnect(api_key=cred['api_key'])

try:
    session_key = autologin.get_session_key(cred=cred, force=False)
except:
    session_key = autologin.get_session_key(cred=cred, force=True)
    
    
breeze.generate_session(api_secret=cred['api_secret'],
                        session_token=session_key)
###################################################################


####### CONTAINS PAST EXPIRY LIST ##########
with open('expiries.json', 'r') as file:
    expiries = json.load(file)
############################################


expiry_date = "06-Dec-2023" # 'expiries.json' contains a list of expiry dates in this format
start_datetime = "06-Dec-2023 9:15:00" 
end_datetime = "06-Dec-2023 15:29:59" 

Breezy.fetch_data(
                api = breeze,
                scrip = "CNXBAN",  # 'NIFTY' for Nifty 50 | 'CNXBAN' for Bank Nifty | 'NIFFIN' for Finnifty | 'NIFMID' for Midcap Nifty
                exch = "NFO",
                expiry_date = datetime.strptime(expiry_date, "%d-%b-%Y"),
                start_datetime = datetime.strptime(start_datetime, "%d-%b-%Y %H:%M:%S"),
                end_datetime = datetime.strptime(end_datetime, "%d-%b-%Y %H:%M:%S"),
                start_strike = 47000,
                end_strike = 47200,
                step = 100,
                max_threads = 3, #Set this to 1 if you are getting api breeze_historical_v2() error
                export_path = 'HistoricData/' #will auto-create path if it doesn't exist
                )

unix_end = time.time()
print(f"Time elapsed: {unix_end - unix_start} seconds")