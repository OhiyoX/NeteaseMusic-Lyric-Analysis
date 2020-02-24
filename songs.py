from bs4 import BeautifulSoup
import re
import functions as func


class Songs:
    def __init__(self):
        # 初始歌单
        self.songs = {}
        self.songs['id'] = []
        self.songs['name'] = []
        self.songs['url'] = []
        self.only_lyric = []

    def get_plist(self, url, st):
        # 建立歌单
        content = func.get_page(url).text
        # 新建bs对象
        soup = BeautifulSoup(content, 'lxml')
        plist = soup.find(name='ul',
                          attrs={'class': 'f-hide'})
        # 根据toggle传递csv文件名
        if st.toggle == False:
            st.csv_fname = st.playlist_title = soup.find(name='h2', class_='f-ff2').string
        # 筛选数据
        for song in plist.find_all(name='li'):
            # id
            id = re.search('=([0-9]+)', song.a['href'])
            # 避免重复记录歌名
            id_foo = id.group(1)
            if id_foo not in self.songs['id']:
                self.songs['id'].append(id_foo)
                # name
                song_name = song.a.string
                self.songs['name'].append(song_name)
                # url
                song_url = 'https://music.163.com' + song.a['href']
                self.songs['url'].append(song_url)

    def get_lyric(self):
        """获得歌词"""
        self.songs['lyric'] = []
        total = len(self.songs['id'])
        for song_id in self.songs['id']:
            url = 'http://music.163.com/api/song/lyric?os=pc&id=' \
                  + song_id \
                  + '&lv=-1&kv=-1&tv=-1'
            # 获得歌词内容
            content = func.get_page(url).json()
            if 'lrc' in content and 'nolyric' not in content and content['lrc'] is not None:
                lyric = content['lrc']['lyric']
                # 清洗歌词
                lyric = re.sub('\[.*?\]', '', lyric)
                self.songs['lyric'].append(lyric)
                self.only_lyric.append(lyric)
                print('completed ' + str(round(self.songs['id'].index(song_id) / total * 100, 2)) + '% ', end='')
                print('added lyric id: ' + song_id)
            else:
                # 填充，避免出现浮点数的空值
                self.songs['lyric'].append('ThisShallBeIgnored')
