from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib
import pyotp
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

    
try:
    service = Service(ChromeDriverManager().install())
except ValueError:
    latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
    service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())

def get_session_key(cred, force=False):
    
    if not os.path.exists('session_key.txt'):
        with open('session_key.txt', 'w') as file:
            file.write('')  # Creating an empty file
    
    if force == False:
        
        with open("session_key.txt", 'r') as file:
            content = file.read().strip()
            splitted_content = (content.split(','))
            content_date = splitted_content[1].strip()
            old_session_key = splitted_content[0]
            
            if content_date == datetime.today().strftime('%Y-%m-%d'):
                print("Key already generated for today", content_date)
                return old_session_key

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run in headless mode without GUI

    # Create the WebDriver with the specified options
    print("Generating new key.....")
    driver = webdriver.Chrome(options = chrome_options)
    # Navigate to the login page of the website
    driver.get("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(cred['api_key']))

    # Find the username and password input fields using their HTML attributes
    driver.find_element(By.XPATH, '//*[@id="txtuid"]').send_keys(cred['username'])
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="txtPass"]').send_keys(cred['password'])
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="chkssTnc"]').click()
    time.sleep(0.2)
    driver.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
    time.sleep(0.2)

    # Entering totp
    otp = pyotp.TOTP(cred['totp_key']).now()

    for position, digit in zip(range(1,7), otp):
        driver.find_element(By.XPATH, f'//*[@id="pnlOTP"]/div[2]/div[2]/div[3]/div/div[{position}]/input').send_keys(digit)
        time.sleep(0.1)

    driver.find_element(By.XPATH, '//*[@id="Button1"]').click()
    time.sleep(0.5)
    # Getting session key
    newurl = driver.current_url
    time.sleep(0.3)
    session_key = newurl[newurl.index('=')+1:]
    with open("session_key.txt", 'w') as a:
            a.write(f'{session_key}, {datetime.today().strftime("%Y-%m-%d")}')
    driver.quit()
    print("Key Generated")
    return session_key
