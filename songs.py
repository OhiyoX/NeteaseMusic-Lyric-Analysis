from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import re
import pandas
import functions as func


class Songs:
    def __init__(self):
        # 初始歌单
        self.list_title = ''
        self.songs = {}
        self.songs['id'] = []
        self.songs['name'] = []
        self.songs['url'] = []
        self.only_lyric = []

    def get_plist(self, url):
        # 建立歌单:name与url
        content = func.get_page(url).text
        # 新建bs对象
        soup = BeautifulSoup(content, 'lxml')
        plist = soup.find(name='ul',
                          attrs={'class': 'f-hide'})
        self.list_title = soup.find(name='h2', class_='f-ff2').string
        # 筛选数据
        for song in plist.find_all(name='li'):

            # id
            id = re.search('=([0-9]+)', song.a['href'])
            self.songs['id'].append(id.group(1))
            # name
            song_name = song.a.string
            self.songs['name'].append(song_name)
            # url
            song_url = 'https://music.163.com' + song.a['href']
            self.songs['url'].append(song_url)


    def songs_to_csv(self):
        """输出为csv"""
        df = pandas.DataFrame({'song_id': self.songs['id'],
                               'song_name': self.songs['name'],
                               'song_url': self.songs['url'],
                               'song_lyric': self.songs['lyric']})
        df.to_csv(self.list_title + '.csv', index=False, sep=',', encoding='UTF-8')

    def get_lyric(self):
        """获得歌词"""
        self.songs['lyric'] = []
        for song_id in self.songs['id']:
            url = 'http://music.163.com/api/song/lyric?os=pc&id=' \
                  + song_id \
                  + '&lv=-1&kv=-1&tv=-1'
            # 获得歌词内容
            content = func.get_page(url).json()
            if 'lrc' in content:
                lyric = content['lrc']['lyric']
                # 清洗歌词
                lyric = re.sub('\[.*?\]', '', lyric)
                self.songs['lyric'].append(lyric)
                self.only_lyric.append(lyric)
            else:
                # 填充，避免出现浮点数的空值
                self.songs['lyric'].append('ThisShallBeIgnored')
