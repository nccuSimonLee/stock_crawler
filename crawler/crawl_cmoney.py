import jsonlines
from cmoney_api import crawl_stock


def main():
    channel_id = None
    unknown_id = '1622375252845'

    with open('../stock_lists/top_30_stock.txt', 'r') as f:
        stock_list = f.read().splitlines()

    for stock_id in stock_list:
        with jsonlines.open(f'../articles/{stock_id}.jsonl', 'w') as f:
            for res in crawl_stock(channel_id, unknown_id, stock_id):
                f.write_all(res)

if __name__ == '__main__':
    main()