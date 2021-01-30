from songs import Songs, Playlists
from wordpool import WordPool
from settings import Settings
import functions as func

import os

st = Settings


def search_and_save():
    pls = Playlists(keyword=st.search_keyword,
                    limit=st.result_limit)
    # 获得前50项歌单
    pls.get_playlists()
    # 递归下载歌单
    pls.recur_playlists()
    if not os.path.exists('res/' + st.csv_fname + '-with-lyrics.csv'):
        pls.get_lyric()


def single_playlist():
    if not os.path.exists('res/' + st.csv_fname + '.csv'):
        # 新建一个歌单类
        s = Songs(keyword=st.search_keyword,
                  limit=st.result_limit)
        s.get_plist_songs(st.playlist_url)
        s.get_lyric()


if __name__ == "__main__":
    if st.toggle:
        search_and_save()
    else:
        single_playlist()
    # 新建一个词池
    w = WordPool()
    w.get_wordpool()
    if st.word_rank:
        w.word_freq()
        w.get_tag_rate()
    w.generate_wordcloud()
