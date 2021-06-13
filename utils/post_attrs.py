from bs4 import BeautifulSoup as bs, NavigableString
from datetime import datetime, timedelta
from snownlp import SnowNLP
from opencc import OpenCC
import numpy as np
from .adjust_time import cmoney_time_to_dt, ptt_time_to_dt, adjust_dt



T2S = OpenCC('t2s')

def compute_sentiments(content):
    if not content:
        return 0.5
    return SnowNLP(T2S.convert(content)).sentiments


class CmoneyAttrs:
    def __init__(self, post):
        self.id = post['ArtId']
        self.stock = post['MentionTags'][0]['CommKey']
        self.like_count = int(post['ArtLkdCnt'])
        self.reply_count = int(post['ArtRepdCnt'])
        self.content = self.extract_content(post['ArtCtn'])
        self.char_count = len(self.content.replace('\n', ''))
        self.adjst_dt = adjust_dt(cmoney_time_to_dt(post['ArtCteTm']))
        self.sentiments = compute_sentiments(self.content)

    @classmethod
    def extract_content(cls, post_ctn):
        content = []
        soup = bs(post_ctn, 'html.parser')
        for child in soup.select_one('.main-content').children:
            if type(child) == NavigableString:
                content.append(child)
            elif child.text:
                content.append(child.text)
        return '\n'.join(content)


class CommentsSentiments:
    def __init__(self, comments):
        self.scores = np.array(
            [compute_sentiments(comment['message'])
             for comment in comments]
        )
        self.mean = np.mean(self.scores)
        self.median = np.median(self.scores)
        self.std = np.std(self.scores)
        self.pushs = np.array([-1 if comment['push'] == '噓' else 1
                               for comment in comments])


def filter_ptt_comments(comments, post_dt):
    filtered_comments = []
    deadline = get_dead_line(post_dt)
    for comment in comments:
        time_str = f'{post_dt.year}/{comment["time"]}'
        try:
            comment_dt = datetime.strptime(time_str, '%Y/%m/%d %H:%M')
        except:
            continue
        if comment_dt < deadline:
            filtered_comments.append(comment)
    return filtered_comments

def get_dead_line(post_dt):
    deadline = datetime(post_dt.year, post_dt.month, post_dt.day, 13, 30, 0)
    deadline += timedelta(days=1)
    return deadline


class PttAttrs:
    def __init__(self, post):
        self.id = post['id']
        self.stock = post['stock'][0]
        self.push_count = sum(cmt['push'] == '推' for cmt in post['comment'])
        self.reply_count = len(post['comment'])
        self.content = post['content']
        self.char_count = len(self.content.replace('\n', ''))
        self.adjst_dt = adjust_dt(ptt_time_to_dt(post['time']))
        self.sentiments = compute_sentiments(self.content)

        filtered_comments = filter_ptt_comments(post['comment'], self.adjst_dt)
        self.comments_sentiments = CommentsSentiments(filtered_comments)
