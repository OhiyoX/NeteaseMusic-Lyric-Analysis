import functions as func
import json

class Playlist:
    def __init__(self):
        self.playlists = []

    def get_playlists(self, search):
        # 保留前50项
        url = 'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={' \
              + search + '}&type=1000&offset=0&total=true&limit=50'
        text = func.get_page(url)
        p_json = json.load(text)
        result = p_json['result']
        self.playlists = result['playlists']
