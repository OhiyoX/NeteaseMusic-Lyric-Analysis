import functions as func
import json
from songs import Songs
import time


class Playlists(Songs):
    def __init__(self):
        super().__init__()
        self.playlists = []
        self.keyword = ''

    def get_playlists(self, st):
        try:
            with open('res/'+st.search_keyword+'.json', encoding='UTF-8') as f:
                p_json = json.load(f)
        except FileNotFoundError:
            url = 'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={' \
                  + st.search_keyword + '}&type=1000&offset=0&total=true&limit=' + str(st.result_limit)
            p_json = func.get_page(url).json()
            with open('res/'+st.search_keyword+'.json', 'w', encoding='UTF-8') as k:
                text = json.dumps(p_json, ensure_ascii=False)
                k.write(text)
        result = p_json['result']
        self.playlists = result['playlists']

    def recur_playlists(self, st):
        """递归获取歌单列表"""
        for playlist in self.playlists:
            url = 'https://music.163.com/#/playlist?id=' + str(playlist['id'])
            self.get_plist(url, st)
            print('completed ' + str(self.playlists.index(playlist) / len(self.playlists) * 100) + '%')
            time.sleep(2)
        self.get_lyric()
        func.songs_to_csv(self.songs, st)
