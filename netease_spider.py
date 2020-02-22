from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import re
import pandas


def download(url):
    """获得歌单列表"""
    # 处理链接
    url = re.sub('/#', '', url)

    # 设置头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    # 尝试获取
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None


def get_plist(url):
    # 建立歌单name与url
    content = download(url)
    # 新建bs对象
    soup = BeautifulSoup(content, 'lxml')
    plist = soup.find(name='ul',
                      attrs={'class': 'f-hide'})
    # 初始歌单
    songs = {}
    songs['id'] = []
    songs['name'] = []
    songs['url'] = []

    for song in plist.find_all(name='li'):
        song_id = re.match('\d+', song.a['href'])
        songs['id'] = song_id
        song_name = song.a.string
        songs['name'].append(song_name)
        song_url = 'https://music.163.com' + song.a['href']
        songs['url'].append(song_url)

    # 输出为csv
    df = pandas.DataFrame({'song_id': songs['id'],
                           'song_name': songs['name'],
                           'song_url': songs['url']})
    df.to_csv('plist.csv', index=False, sep=',', encoding='UTF-8')
    return songs


def get_lyric(songs):
    """获得歌词"""
    for song_id in songs['id']:
        url = 'http://music.163.com/api/song/lyric?os=pc&id=85580' \
              + song_id \
              + '&lv=-1&kv=-1&tv=-1'

if __name__ == "__main__":

    url = 'https://music.163.com/#/discover/toplist'
    songs = get_plist(url)

