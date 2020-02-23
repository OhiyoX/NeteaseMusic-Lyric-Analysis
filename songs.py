from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import re
import pandas


class Songs:
    def __init__(self):
        # 初始歌单
        self.songs = {}
        self.songs['id'] = []
        self.songs['name'] = []
        self.songs['url'] = []
        self.only_lyric = []

    def get_plist(self, url):
        # 建立歌单:name与url
        content = self.get_page(url).text
        # 新建bs对象
        soup = BeautifulSoup(content, 'lxml')
        plist = soup.find(name='ul',
                          attrs={'class': 'f-hide'})

        # 筛选数据
        for song in plist.find_all(name='li'):
            # id
            id = re.search('=([0-9]+)', song.a['href'])
            self.songs['id'].append(id.group(1))
            # title
            song_name = song.a.string
            self.songs['name'].append(song_name)
            # url
            song_url = 'https://music.163.com' + song.a['href']
            self.songs['url'].append(song_url)

    def get_page(self, url):
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
                return response
        except RequestException:
            return None

    def songs_to_csv(self):
        """输出为csv"""
        df = pandas.DataFrame({'song_id': self.songs['id'],
                               'song_name': self.songs['name'],
                               'song_url': self.songs['url'],
                               'song_lyric': self.songs['lyric']})
        df.to_csv('plist.csv', index=False, sep=',', encoding='UTF-8')

    def get_lyric(self):
        """获得歌词"""
        self.songs['lyric'] = []
        for song_id in self.songs['id']:
            url = 'http://music.163.com/api/song/lyric?os=pc&id=' \
                  + song_id \
                  + '&lv=-1&kv=-1&tv=-1'
            # 获得歌词内容
            content = self.get_page(url).json()
            if 'lrc' in content:
                lyric = content['lrc']['lyric']
                # 清洗歌词
                lyric = re.sub('\[.*?\]', '', lyric)
                self.songs['lyric'].append(lyric)
                self.only_lyric.append(lyric)
            else:
                # 填充，避免出现浮点数的空值
                self.songs['lyric'].append('ThisShallBeIgnored')
