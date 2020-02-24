from wordcloud import WordCloud  # 词云
import pkuseg  # 结巴分词
from matplotlib import pyplot as plt  # 数据可视化库
import re
import pandas
import time
import functions as func
from collections import Counter
from tabulate import tabulate


class WordPool:
    def __init__(self):
        self.word_pool = []
        self.new_word_pool = []
        self.freq = {}

    def get_wordpool(self, st, s=None):
        time_start = time.time()
        seg = pkuseg.pkuseg()
        print('start processing')
        """获得分词组"""
        if s is not None:
            lyrics = ' '.join(s.only_lyric)
        # 可以直接处理，这里为了与下载分离，使用导入文件的形式
        else:
            with open('res/' + st.csv_fname + '.csv', encoding='UTF-8') as p:
                songs = pandas.read_csv(p)
                text = songs['song_lyric'].tolist()
                print('You have ' + str(len(text)) + ' songs')
                lyrics = ' '.join(text)
        reg = re.compile('\\n|/|-+|～+|&|\*+')
        lyrics = re.sub(reg, ' ', lyrics)
        self.word_pool = seg.cut(lyrics)

        self.filter_words(st.more)
        time_end = time.time()
        print('time past: ', time_end - time_start, 's')

    def generate_wordcloud(self):
        # 根据词频生成词云
        plt.figure(figsize=(16, 20), dpi=200)
        wordcloud = WordCloud(
            font_path="FZYouHK_506L.TTF",
            background_color="white",
            width=1600,
            height=2000,
            max_font_size=600,
            margin=2).generate_from_frequencies(self.freq)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    def word_freq(self, st):
        print('start ranking')
        foo = []
        for word in self.new_word_pool:
            if len(word) >= 2:
                foo.append(word)
        freq = Counter(foo).most_common(len(self.new_word_pool))
        w1, w2, n1, n2 = [], [], [], []
        for i in range(20):
            if i < 10:
                w1.append(freq[i][0])
                n1.append(freq[i][1])
            else:
                w2.append(freq[i][0])
                n2.append(freq[i][1])
        for r in freq:
            self.freq[r[0]] = r[1]
        df = pandas.DataFrame({'前1-10': w1, '-次数': n1, '前11-20': w2, '次数-': n2}).set_index('前1-10')
        print(tabulate(df, tablefmt="pipe", headers="keys"))

    def filter_words(self, more=None):
        """修剪词语"""
        """
        useless = [' ', 'thisshallbeignored', '作曲', '作词', '制作', '混音', '编曲', 'publishing', '录音室',
                   '录音室', '监制', '原唱', '弦乐', '配唱', '有限公司', '录音师', '作品', '企划', '音乐', '策划',
                   '编写', '吉他', 'studio', '制作 ', '母带', '钢琴', '贝斯', '鼓手', '网易', '录音',
                   'seem', 'right', 've', 'got', 'won', '工作室', 'gonna', 'll', 're', 'might', 'ain',
                   'don', 'still', 'cause', 'hey', 'give', 'past', 'will', 'gotta']
        """
        print('start filtering')
        useless = ['da', 'doo', 'ya', 'oh', 'ooh', 'la', 'ayy', 'woah', 'na', 'ah', 'nah',
                   'yeah','hey']
        with open('res/stoplist.txt', encoding='UTF-8') as f:
            stoplist = f.read().splitlines()  # 不能用readlines(),因为会有换行符
        if more == 'm':
            sdf = stoplist+useless
            self.new_word_pool = func.make_filter(self.word_pool, sdf)
        elif more == 'e':
            with open('res/stoplist-e.txt', encoding='UTF-8') as f:
                stopen = f.read().splitlines()  # 不能用readlines(),因为会有换行符
                eef = stoplist+stopen+useless
            self.new_word_pool = func.make_filter(self.word_pool, eef)
        else:
            self.new_word_pool = func.make_filter(self.word_pool, stoplist)
