from songs import Songs
from playlists import Playlists
from wordpool import WordPool
from settings import Settings
import functions as func


def search_and_save():
    pls = Playlists()
    # 获得前50项歌单
    pls.get_playlists(st)

    # 递归下载歌单
    pls.recur_playlists(st)


def single_playlist(w):
    try:
        with open(st.csv_fname + '.csv') as p:
            pass
    except FileNotFoundError:
        # 新建一个歌单类
        s = Songs()
        s.get_plist(st.playlist_url, st)
        s.get_lyric()
        func.songs_to_csv(s.songs, st)

    w.get_word_pool(st)
    w.make_wordcloud()




if __name__ == "__main__":
    st = Settings()
    # 新建一个词池
    w = WordPool()

    if st.toggle == True:
        search_and_save()
    else:
        single_playlist(w)

    w.get_word_pool(st)
    w.make_wordcloud()