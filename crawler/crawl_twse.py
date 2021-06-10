from stock_price_api import crawl_and_save_months_prices



RAW_FIELDS = ['日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']
        

def main():
    with open('../stock_lists/new_top_30_stock.txt', 'r') as f:
        stock_list = f.read().splitlines()

    for stock in stock_list:
        with open(f'../prices/{stock}.csv', 'w') as f:
            f.write('year,month,day,volume,turnover,open,high,low,close,change,transaction\n')
            for price in crawl_and_save_months_prices(stock, 2021, range(5, 0, -1)):
                f.write(f'{",".join(price)}\n')

            for price in crawl_and_save_months_prices(stock, 2020, range(12, 0, -1)):
                f.write(f'{",".join(price)}\n')

if __name__ == '__main__':
    main()
