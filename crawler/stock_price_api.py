import requests



def request_twse_prices(stock_id, year, month):
    params = {
        'response': 'json',
        'date': f'{year}{str(month).zfill(2)}01',
        'stockNo': stock_id,
        '_': '1622511559599'
    }
    api = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY'
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    res = requests.get(api, params=params, headers=headers)
    return res

def request_tpex_prices(stock_id, year, month):
    params = {
        'l': 'zh-tw',
        'd': f'{year - 1911}/{str(month).zfill(2)}',
        'stkno': stock_id,
        '_': '1622604093726'
    }
    api = f'https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php'
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    res = requests.get(api, params=params, headers=headers)
    return res
