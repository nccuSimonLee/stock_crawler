import requests
from bs4 import BeautifulSoup as bs



def crawl_stock(channel_id, unknown_id, stock_id):
    channel_id = channel_id or stockId_to_channelId(stock_id)
    res = request_stockv2(channel_id, unknown_id)
    res = sorted(res.json(), key=lambda x: -int(x['ArtId']))
    yield res
    last_art_id = res[-1]['ArtId']
    last_cte_time = res[-1]['ArtCteTm']

    req_cnt = 1
    while not stop_crawl(last_cte_time, req_cnt):
        print(f'{stock_id} - {req_cnt} - last article id: {last_art_id}')
        res = request_moreofstockv2(channel_id, unknown_id, last_art_id)
        res = sorted(res.json(), key=lambda x: -int(x['ArtId']))
        if not res:
            break
        yield res
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

def request_stockv2(channel_id, unknown_id):
    params = {
        'articleCategory': 'Personal',
        'channelId': channel_id,
        'size': '500',
        'sTime': '',
        'articleSortType': 'latest',
        'articleSortCount': '0',
        'isIncludeLimitedAskArticle': 'false',
        '_': unknown_id
    }
    api = 'https://www.cmoney.tw/follow/channel/getdata/articlelistofstockv2'
    res = requests.get(api, params=params)
    return res

def request_moreofstockv2(channel_id, unknown_id, start_article_id):
    params = {
        'articleCategory': 'Personal',
        'channelId': channel_id,
        'articleId': start_article_id,
        'size': '500',
        'skipCount': '0',
        'articleSortCount': '0',
        'sTime': '',
        'articleSortType': 'latest',
        'isIncludeLimitedAskArticle': 'false',
        '_': unknown_id
    }
    api = 'https://www.cmoney.tw/follow/channel/getdata/articlelistmoreofstockv2'
    res = requests.get(api, params=params)
    return res

def stockId_to_channelId(stock_id):
    res = requests.get(f'https://www.cmoney.tw/follow/channel/stock-{stock_id}?chart=d&type=Personal')
    soup = bs(res.text, 'html.parser')
    data = eval(soup.select_one('#PageData').text.replace('null', 'None'))
    channel_id = data['StockInfo']['ChannelId']
    return channel_id
