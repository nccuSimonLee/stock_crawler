import requests
import time



def crawl_and_save_months_prices(stock_id, year, months, stock_type='twse'):
    assert stock_type in {'twse', 'tpex'}
    price_key = 'data' if stock_type == 'twse' else 'aaData'
    for month in months:
        print(f'{stock_id} - {year} - {month}')
        if stock_type == 'twse':
            results = request_twse_prices(stock_id, year, month).json()
        else:
            results = request_tpex_prices(stock_id, year, month).json()
        if no_data(results, stock_type):
            time.sleep(10)
            continue
        for price in preprocess_prices(results[price_key], stock_type):
            yield price
        time.sleep(10)
    return

def preprocess_prices(prices, stock_type='twse'):
    assert stock_type in {'twse', 'tpex'}
    preprocessed_prices = []
    for price in prices:
        year, month, day = price[0].split('/')
        year = str(int(year) + 1911)
        price = [p.replace(',', '') for p in price[1:]]
        if stock_type == 'tpex':
            for i in range(2):
                # 因為前兩項是仟股、仟元
                price[i] = str(int(price[i]) * 1000)
        price[-2] = price[-2].replace('+', '')
        price = [year, month, day] + price
        preprocessed_prices.append(price)
    return preprocessed_prices

def no_data(results, stock_type):
    return ((stock_type == 'twse' and results.get('stat', '') == '很抱歉，沒有符合條件的資料!')
            or (stock_type == 'tpex' and not results['aaData']))

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
