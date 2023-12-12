import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta, datetime, timezone

def print_results(results):
    successful_strikes = [f"{strike} {opt_type.upper()}" for (strike, opt_type), success in results.items() if success]
    unsuccessful_strikes = [f"{strike} {opt_type.upper()}" for (strike, opt_type), success in results.items() if not success]

    print("Successful strikes:", successful_strikes)
    print("Unsuccessful strikes:", unsuccessful_strikes)
    
def format_expiry_date(expiry_datetime):
    # Assure the time is set to 06:00:00
    expiry_datetime = expiry_datetime.replace(hour=6, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

    # Convert to the desired format
    formatted_date = expiry_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return formatted_date

def download_and_save_data(api, scrip, exch, strike_price, right, expiry_date, start_datetime, end_datetime, interval, export_path):
    
    try:
        full_data = []
        current_start_time = start_datetime

        while current_start_time < end_datetime:
            next_end_time = min(current_start_time + timedelta(seconds=999), end_datetime)
            
            data = api.get_historical_data_v2(interval=interval,
                                    from_date=current_start_time,
                                    to_date=next_end_time,
                                    stock_code=scrip,
                                    exchange_code=exch,
                                    product_type="options",
                                    expiry_date=expiry_date,
                                    right=right,
                                    strike_price=str(strike_price)) # Sample response structure

            if isinstance(data, dict) and 'Success' in data:
                # If this is the first loop iteration and data is not empty, store the headers
                if not full_data and data['Success']:
                    headers = data['Success'][0].keys()
                    full_data.append(headers)
                
                # Add data values
                for item in data['Success']:
                    full_data.append(item.values())
            
            current_start_time = next_end_time
            
        expiry_date_obj = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
        expiry_month = expiry_date_obj.strftime("%B")
        expiry_year = expiry_date_obj.strftime("%Y")

        dir_name = f"{export_path}/{scrip}/{expiry_year}/{expiry_month}/{expiry_date.split('T')[0]}_expiry"
        os.makedirs(dir_name, exist_ok=True)

        option_type = "CE" if right == "call" else "PE"
        file_name = f"{dir_name}/{strike_price}_{option_type}.csv"

        with open(file_name, 'w') as file:
            for row in full_data:
                file.write(','.join(map(str, row)) + '\n')
            print(f'{file_name} written')   
        return (True, strike_price)
    
    except Exception as e:
        print(f"{strike_price} failed.{e}")
        return (False, strike_price)


def fetch_data(api,
               scrip,
               exch,
               expiry_date,
               start_datetime,
               end_datetime,
               start_strike,
               end_strike,
               step,
               max_threads = 3,
               interval = "1second",
               export_path = "HistoricData"):
    
    
    expiry_date = format_expiry_date(expiry_date)
    strikes = range(start_strike, end_strike + 1, step)
    
    def run_download_and_track_results(strikes):
        results = {}
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_strike = {(executor.submit(download_and_save_data, api, scrip, exch, strike, opt_type, expiry_date, start_datetime, end_datetime, interval, export_path), strike, opt_type) for strike in strikes for opt_type in ['call', 'put']}

            for future, strike, opt_type in future_to_strike:
                success, _ = future.result()
                results[(strike, opt_type)] = success
                
                ### Print the result for each strike
                status_msg = "completed" if success else "failed"
                # print(f"Strike {strike} {opt_type.upper()} download and save {status_msg}")

        return results

    # First attempt
    print("Running first attempt...")
    results = run_download_and_track_results(strikes)

    # Retry unsuccessful attempts
    unsuccessful_attempts = [(strike, opt_type) for (strike, opt_type), success in results.items() if not success]
    if unsuccessful_attempts:
        print("Retrying unsuccessful attempts...")
        retry_results = run_download_and_track_results([strike for strike, _ in unsuccessful_attempts])
        results.update(retry_results)

    # Final results
    print_results(results)