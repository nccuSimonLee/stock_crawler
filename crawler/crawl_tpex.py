from stock_price_api import crawl_and_save_months_prices



def main():

    stock_list = ['3105', '4743', '6547']

    for stock in stock_list:
        with open(f'../prices/{stock}.csv', 'w') as f:
            f.write('year,month,day,volume,turnover,open,high,low,close,change,transaction\n')
            for price in crawl_and_save_months_prices(stock, 2021, range(5, 0, -1), 'tpex'):
                f.write(f'{",".join(price)}\n')

            for price in crawl_and_save_months_prices(stock, 2020, range(12, 0, -1), 'tpex'):
                f.write(f'{",".join(price)}\n')

if __name__ == '__main__':
    main()
