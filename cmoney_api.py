import requests
from bs4 import BeautifulSoup as bs



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
