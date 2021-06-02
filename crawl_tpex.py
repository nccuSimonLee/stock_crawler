from stock_price_api import request_tpex_prices
import time




def crawl_and_save_months_prices(stock_id, year, months, f):
    for month in months:
        print(f'{stock_id} - {year} - {month}')
        results = request_tpex_prices(stock_id, year, month).json()
        for price in preprocess_prices(results['aaData']):
            f.write(f'{",".join(price)}\n')
        time.sleep(10)
    return

def preprocess_prices(prices):
    preprocessed_prices = []
    for price in prices:
        year, month, day = price[0].split('/')
        year = str(int(year) + 1911)
        price = [p.replace(',', '') for p in price[1:]]
        for i in range(2):
            # 因為前兩項是仟股、仟元
            price[i] = str(int(price[i]) * 1000)
        price[-2] = price[-2].replace('+', '')
        price = [year, month, day] + price
        preprocessed_prices.append(price)
    return preprocessed_prices

def main():

    stock_list = ['3105', '4743', '6547']

    for stock in stock_list:
        with open(f'prices/{stock}.csv', 'w') as f:
            f.write('year,month,day,volume,turnover,open,high,low,close,change,transaction\n')
        f = open(f'prices/{stock}.csv', 'a')
        crawl_and_save_months_prices(stock, 2021, range(5, 0, -1), f)
        crawl_and_save_months_prices(stock, 2020, range(12, 0, -1), f)

if __name__ == '__main__':
    main()
