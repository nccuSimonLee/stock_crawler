import jsonlines
from cmoney_api import (request_stockv2,
                        request_moreofstockv2,
                        stockId_to_channelId)


def crawl_stock(channel_id, unknown_id, stock_id):
    channel_id = channel_id or stockId_to_channelId(stock_id)
    res = request_stockv2(channel_id, unknown_id)
    res = sorted(res.json(), key=lambda x: -int(x['ArtId']))
    with jsonlines.open(f'articles/{stock_id}.jsonl', 'w') as f:
        f.write_all(res)
    last_art_id = res[-1]['ArtId']
    last_cte_time = res[-1]['ArtCteTm']

    f = jsonlines.open(f'articles/{stock_id}.jsonl', 'a')
    req_cnt = 1
    while not stop_crawl(last_cte_time, req_cnt):
        print(f'{stock_id} - {req_cnt} - last article id: {last_art_id}')
        res = request_moreofstockv2(channel_id, unknown_id, last_art_id)
        res = sorted(res.json(), key=lambda x: -int(x['ArtId']))
        if not res:
            break
        f.write_all(res)
        last_art_id = res[-1]['ArtId']
        last_cte_time = res[-1]['ArtCteTm']
        req_cnt += 1
    return

def stop_crawl(last_cte_time, req_cnt):
    return (
        last_cte_time.startswith('2020/01/01')
        or int(last_cte_time[:4]) < 2020
        or req_cnt >= 2000
    )

def main():
    channel_id = None
    unknown_id = '1622375252845'

    with open('top_30_stock.txt', 'r') as f:
        stock_list = f.read().splitlines()
    
    for stock_id in stock_list:
        if stock_id == '2603':
            continue
        crawl_stock(channel_id, unknown_id, stock_id)

if __name__ == '__main__':
    main()