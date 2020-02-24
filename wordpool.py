
from wordcloud import WordCloud # 词云
import jieba # 结巴分词
from matplotlib import pyplot as plt # 数据可视化库
import re
import pandas
from collections import Counter


class WordPool:
    def __init__(self):
        self.word_pool = []

    def get_word_pool(self, st, s=None):
        """获得分词组"""
        if s is not None:
            lyrics = ' '.join(s.only_lyric)
        # 可以直接处理，这里为了与下载分离，使用导入文件的形式
        else:
            with open(st.csv_fname + '.csv', encoding='UTF-8') as p:
                songs = pandas.read_csv(p)
                text = songs['song_lyric'].tolist()
                print('You have ' + str(len(text)) + ' songs')
                lyrics = ' '.join(text)
        lyrics = re.sub('\\n|\[|:|\)', ' ', lyrics)
        self.word_pool = jieba.lcut(lyrics)

        self.filter_words(st.more)

    def make_wordcloud(self):
        plt.figure(figsize=(16, 20), dpi=200)
        result = ' '.join(self.word_pool)
        wordcloud = WordCloud(font_path="FZSSK.TTF", background_color="white", width=1600, height=2000, margin=2).generate(result)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()


    def filter_words(self, more=None):
        """修剪词语"""
        useless = ['ThisShallBeIgnored', '作曲', '作词', '制作', '混音', '编曲', 'Publishing', '录音室',
                   '混音 母带', '录音室', '监制', '原唱', '弦乐', '配唱', '有限公司', '录音师', '作品', '企划', '音乐', '策划',
                   '编写', '吉他', 'Studio', '制作 ', '母带', '钢琴', '贝斯', '鼓手', '网易', '录音', '工作室']
        useless2 = ['Da', 'doo', 'ya', 'oh', 'ooh', 'la', 'ayy', 'Woah']

        if more == 'more':
            for word in self.word_pool:
                if word in useless:
                    self.word_pool.remove(word)
                if word in useless2:
                    self.word_pool.remove(word)
        elif more == 'mmore':
            with open('百度停用词表.txt', encoding='UTF-8') as f:
                stoplist = f.read().splitlines() # 不能用readlines(),因为会有换行符
            for word in self.word_pool:
                if word in stoplist:
                    self.word_pool.remove(word)
        else:
            for word in self.word_pool:
                if word in useless:
                    self.word_pool.remove(word)
