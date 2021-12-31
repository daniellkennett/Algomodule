
from tda import auth, client
import json
from TDameritrad_api import CONSUMER_KEY, REDIRECT_URI, JSON_PATH

token_path = JSON_PATH
api_key = CONSUMER_KEY
# @AMER.OAUTHAP'
redirect_uri = REDIRECT_URI
try:
    c = auth.client_from_token_file(token_path, api_key)
except:
    from selenium import webdriver
    with webdriver.Chrome('/home/daniel/chromedriver') as driver:
        c = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)

r = c.get_price_history('AAPL',
        period_type=client.Client.PriceHistory.PeriodType.YEAR,
        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
        frequency=client.Client.PriceHistory.Frequency.DAILY)
assert r.status_code == 200, r.raise_for_status()
print(json.dumps(r.json(), indent=4))
