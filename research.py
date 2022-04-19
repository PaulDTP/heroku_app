#import tda-api
import pandas as pd
import numpy as np

aapl_day = pd.read_json("/Users/paulterrell-perica/Desktop/Zeppelin/z-algo/data/aapl-2021-07-22.json")





""" 
callback = "http://localhost"

def auth_func():

    token_path = 'token.pickle'
    try:
        c = auth.client_from_token_file(token_path, API_KEY)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(ChromeDriverManager().install()) as driver:
            c = auth.client_from_login_flow(
                driver, API_KEY, CALLBACK_URL, token_path)

    return c


from tda import auth, client
import json

token_path = '/path/to/token.json'
api_key = 'YOUR_API_KEY@AMER.OAUTHAP'
redirect_uri = 'https://your.redirecturi.com'
try:
    c = auth.client_from_token_file(token_path, api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)

r = c.get_price_history('AAPL',
        period_type=client.Client.PriceHistory.PeriodType.YEAR,
        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
        frequency=client.Client.PriceHistory.Frequency.DAILY)
assert r.status_code == 200, r.raise_for_status()
print(json.dumps(r.json(), indent=4)) """