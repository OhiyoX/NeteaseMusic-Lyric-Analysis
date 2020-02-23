
from wordcloud import WordCloud # 词云
import jieba # 结巴分词
import matplotlib.pyplot as plt # 数据可视化库
import re
import pandas

def make_wordcloud(s=None):
    # 制作词图
    if s is not None:
        text = ' '.join(s.only_lyric)
    # 可以直接处理，这里为了与下载分离，使用导入文件的形式
    else:
        with open('plist.csv', encoding='UTF-8') as p:
            songs = pandas.read_csv(p)
            text = songs['song_lyric'].tolist()
            lyrics = ' '.join(text)
    lyrics = re.sub('\\n', ' ', lyrics)
    word_pool = jieba.cut(lyrics)

    # 去除无意义词语
    print(word_pool)
    wordcloud = WordCloud(font_path="FZSSK.TTF", background_color="white",width=1000, height=1000, margin=2).generate(word_pool)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.figure(dpi=200)
    plt.show()

def filter_words(word_pool):
    """修剪词语"""
    useless = ['ThisShallBeIgnored', '作曲', '作词', '制作', '混音', '编曲', 'Music Publishing', '录音室',
               '混音 母带', '录音室', '监制', '原唱', '弦乐', '配唱', '有限公司']

    for word in word_pool:
        if word in useless:
            del word