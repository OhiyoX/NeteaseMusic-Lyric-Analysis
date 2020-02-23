from songs import Songs
from analysis import WordPool

if __name__ == "__main__":

    url = 'https://music.163.com/#/discover/toplist?id=3778678'
    opt = input('already have playlist file?')
    if opt == 'n':
        # 新建一个歌单类
        s = Songs()
        s.get_plist(url)
        s.get_lyric()
        s.songs_to_csv()
        # 新建一个词池
        w = WordPool()
        w.get_word_pool(s)
        w.make_wordcloud()
    else:
        w = WordPool()
        w.get_word_pool()
        w.make_wordcloud()



