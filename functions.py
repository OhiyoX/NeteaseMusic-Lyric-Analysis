# pip install requests pandas
import requests
from requests.exceptions import RequestException
import re
import pandas


def get_page(url):
    """获得网页"""
    # 处理链接
    url = re.sub('/#', '', url)

    # 设置头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    # 尝试获取
    flag = 5
    while flag > 0:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flag = 0
                return response
        except RequestException:
            flag -= 1
            print('retry')
            if flag <= 0:
                return None


def songs_to_csv(songs, st):
    """输出为csv"""
    df = pandas.DataFrame({'song_id': songs['id'],
                           'song_name': songs['name'],
                           'song_url': songs['url'],
                           'song_lyric': songs['lyric']})
    df.to_csv('res/' + st.csv_fname + '.csv', index=False, sep=',', encoding='UTF-8')


def make_filter(word_pool, stoplist):
    # 注意大小写不敏感
    new_word_pool = []
    for word in word_pool:
        l_word = word.lower()
        if l_word not in stoplist:
            new_word_pool.append(l_word)
    return new_word_pool
