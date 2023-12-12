# breeze-historical-options

## Introduction
breeze-historical-options provides traders with second-level historic options data using the ICICI Breeze API. Data can be used for backtesting, analysis and simulation purposes.

## Installation
- Clone or download the repository.
- Install Python and required dependencies: `pip install -r requirements.txt`.

## Usage
- Fill in `cred.yml` with your Breeze API keys and credentials.
- Adjust parameters in `example.py` as needed (e.g., expiry dates, time range, scrip, strike range).
- Run the script: `python example.py`.
- Data will be fetched and saved to the specified path.

## Files Explanation
- `sample_cred.yml`: Template for API credentials.
- `expiries.json`: Contains a list of expiry dates for options data.
- `example.py`: Main script to fetch data using the package.

## Fetch Data Function
```python
from datetime import datetime
from breeze_connect import BreezeConnect
from BreezeHistoricalOptions import autologin, Breezy
import json, yaml, time

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
```
## Login Code
```python
from datetime import datetime
from breeze_connect import BreezeConnect
from BreezeHistoricalOptions import autologin, Breezy
import json, yaml, time

with open('cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    
breeze = BreezeConnect(api_key=cred['api_key'])

try:
    session_key = autologin.get_session_key(cred=cred, force=False)
except:
    session_key = autologin.get_session_key(cred=cred, force=True)
    
    
breeze.generate_session(api_secret=cred['api_secret'],
                        session_token=session_key)
```
## Contributing
Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.
