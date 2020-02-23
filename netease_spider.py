from songs import Songs
from analysis import make_wordcloud

if __name__ == "__main__":

    url = 'https://music.163.com/#/discover/toplist?id=3778678'
    opt = input('already have playlist file?')
    if opt == 'n':
        s = Songs()  # 新建一个歌单类
        s.get_plist(url)
        s.get_lyric()
        s.songs_to_csv()
        make_wordcloud(s)
    else:
        make_wordcloud()



