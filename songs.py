# pip install bs4 lxml

import time
import re
import json
import os

from bs4 import BeautifulSoup
import pandas as pd

import functions as func
from settings import Settings as st


class Songs:
    def __init__(self, keyword,limit):
        # 初始歌单
        self.only_lyric = []
        self.plist = None
        self.keyword = keyword
        self.limit = limit

    def get_plist_songs(self, url):
        if self.plist is None:
            self.plist = pd.DataFrame(columns=['id','name','url'])
        # 建立歌单index
        content = func.get_page(url).text
        # 新建bs对象
        soup = BeautifulSoup(content, 'lxml')
        soup_plist = soup.find(name='ul',
                               attrs={'class': 'f-hide'})
        # 根据toggle传递csv文件名
        if not st.toggle:
            st.csv_fname = st.playlist_title = soup.find(name='h2', class_='f-ff2').string
        # 筛选数据
        songs = {'id': [], 'name': [], 'url': []}
        for song in soup_plist.find_all(name='li'):
            # id
            id = re.search('=([0-9]+)', song.a['href'])
            # 避免重复记录歌名
            id_foo = id.group(1)
            if id_foo not in self.plist['id']:
                songs['id'].append(id_foo)
                # name
                song_name = song.a.string
                songs['name'].append(song_name)
                # url
                song_url = 'https://music.163.com' + song.a['href']
                songs['url'].append(song_url)
                songs['lyric'] = ''
        df = pd.DataFrame(songs,columns=['id', 'name', 'url'])
        self.plist = self.plist.append(df,ignore_index=True)

    def get_lyric(self):
        """获得歌词"""
        file_path = 'res/' + self.keyword + '-build-list.csv'
        if not os.path.exists(file_path):
            print('file not found')
            exit(-1)
        plist = pd.read_csv(file_path)
        plist = plist.drop('Unnamed: 0',axis=1)
        plist_temp = pd.DataFrame(columns=plist.columns)
        total = len(plist['id'])
        n=0
        for index,row in plist.iterrows():
            url = 'http://music.163.com/api/song/lyric?os=pc&id=' \
                  + str(row['id']) \
                  + '&lv=-1&kv=-1&tv='
            # 获得歌词内容

            content = func.get_page(url).json()
            if 'lrc' in content and 'nolyric' not in content and content['lrc'] is not None:
                lyric = content['lrc']['lyric']
                # 清洗歌词
                try:
                    lyric = re.sub('\[.*?\]', '', lyric)
                    row['lyric'] = lyric
                    print('completed ' + str(round(index / total * 100, 2)) + '% ', end='')
                    print('added lyric id: ' + str(row['id']))
                    plist_temp = plist_temp.append(row,ignore_index=True)
                except:
                    continue
            n+=1
            if n == 300:
                break
        plist = plist_temp.copy()
        plist.to_csv('res/'+st.search_keyword + '-with-lyrics.csv', encoding='UTF-8')


class Playlists(Songs):
    def __init__(self,keyword,limit):
        super().__init__(keyword=keyword,limit=limit)
        self.playlists = []

    def get_playlists(self):
        if not os.path.exists('res/'+self.keyword+'.json'):
            url = 'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={' \
                  + self.keyword + '}&type=1000&offset=0&order=hot&total=true&limit=' + str(self.limit)
            json_content = func.get_page(url).json()
            with open('res/' + self.keyword + '.json', 'w', encoding='UTF-8') as f1:
                text = json.dumps(json_content, ensure_ascii=False)
                f1.write(text)
        with open('res/' + self.keyword + '.json', encoding='UTF-8') as f2:
            p_json = json.load(f2)
        result = p_json['result']
        self.playlists = result['playlists']
        return self.playlists

    def recur_playlists(self):
        """递归补充歌单列表、歌曲信息"""
        if not os.path.exists('res/' + self.keyword + '-build-list.csv'):
            time.sleep(2)
            self.plist = pd.DataFrame(columns=['id','name','url'])
            for playlist in self.playlists:
                url = 'https://music.163.com/#/playlist?id=' + str(playlist['id'])
                self.get_plist_songs(url)
                print('completed ' + str(self.playlists.index(playlist) / len(self.playlists) * 100) + '%')
            self.plist.to_csv('res/' + self.keyword + '-build-list.csv', encoding='UTF-8')