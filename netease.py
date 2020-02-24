from songs import Songs
from playlists import Playlists
from wordpool import WordPool
from settings import Settings
import functions as func


def search_and_save():
    pls = Playlists()
    # 获得前50项歌单
    pls.get_playlists(st)

    try:
        with open('res/' + st.csv_fname + '.csv') as f:
            pass
    except FileNotFoundError:
        # 递归下载歌单
        pls.recur_playlists(st)


def single_playlist():
    try:
        with open('res/' + st.csv_fname + '.csv') as p:
            pass
    except FileNotFoundError:
        # 新建一个歌单类
        s = Songs()
        s.get_plist(st.playlist_url, st)
        s.get_lyric()
        func.songs_to_csv(s.songs, st)


if __name__ == "__main__":
    st = Settings()
    # 新建一个词池
    w = WordPool()

    if st.toggle == True:
        search_and_save()
    else:
        single_playlist()
    w.get_wordpool(st)
    if st.word_rank:
        w.word_freq(st)
    w.generate_wordcloud()
