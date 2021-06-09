from stock_price_api import request_twse_prices
import time



RAW_FIELDS = ['日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']

def crawl_and_save_months_prices(stock_id, year, months, f):
    for month in months:
        print(f'{stock_id} - {year} - {month}')
        results = request_twse_prices(stock_id, year, month).json()
        assert results['fields'] == RAW_FIELDS
        for price in preprocess_prices(results['data']):
            f.write(f'{",".join(price)}\n')
        time.sleep(10)
    return

def preprocess_prices(prices):
    preprocessed_prices = []
    for price in prices:
        year, month, day = price[0].split('/')
        year = str(int(year) + 1911)
        price = [p.replace(',', '') for p in price[1:]]
        price[-2] = price[-2].replace('+', '')
        price = [year, month, day] + price
        preprocessed_prices.append(price)
    return preprocessed_prices
        

def main():
    with open('new_top_30_stock.txt', 'r') as f:
        stock_list = f.read().splitlines()
    
    stock_list = ['0050', '2330', '2376', '2409', '2417']

    for stock in stock_list:
        with open(f'prices/{stock}.csv', 'w') as f:
            f.write('year,month,day,volume,turnover,open,high,low,close,change,transaction\n')
        f = open(f'prices/{stock}.csv', 'a')
        crawl_and_save_months_prices(stock, 2021, range(5, 0, -1), f)
        crawl_and_save_months_prices(stock, 2020, range(12, 0, -1), f)
        f.close()

if __name__ == '__main__':
    main()
