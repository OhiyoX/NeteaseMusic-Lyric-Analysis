
from wordcloud import WordCloud # 词云
import jieba # 结巴分词
from matplotlib import pyplot as plt # 数据可视化库
import re
import pandas


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

        # 去除无意义词语，可为空，设置'more'表示强化去除
        self.filter_words('more')

    def make_wordcloud(self):
        plt.figure(figsize=(16, 20), dpi=200)
        result = ' '.join(self.word_pool)
        wordcloud = WordCloud(font_path="FZSSK.TTF", background_color="white", width=1600, height=2000, margin=2).generate(result)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    """排名不会
    def word_rank(self):
        # 词语排名
        # 返回前十的词汇
        rank = Counter(self.word_pool).most_common(10)
        fig, ax = plt.subplots()
        # 设置字体
        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['font.serif'] = ['KaiTi']

        ax.bar(rank.keys(), rank.values())
        ax.set_xlabel("词语")  # 设置x轴标签
        ax.set_ylabel("次数")  # 设置y轴标签
        ax.set_title("网易云热歌唱了什么？")  # 设置标题
        plt.show()
    """

    def filter_words(self, more=None):
        """修剪词语"""
        useless = ['ThisShallBeIgnored', '作曲', '作词', '制作', '混音', '编曲', 'Publishing', '录音室',
                   '混音 母带', '录音室', '监制', '原唱', '弦乐', '配唱', '有限公司', '录音师', '作品', '企划', '音乐', '策划',
                   '编写', '吉他', 'Studio', '制作 ', '母带', '钢琴', '贝斯', '鼓手', '网易 音乐']
        useless2 = ['ThisShallBeIgnored', '作曲', '作词', '制作', '混音', '编曲', 'Music Publishing', '录音室',
                    '混音 母带', '录音室', '监制', '原唱', '弦乐', '配唱', '有限公司', '录音师', '作品', '企划', '音乐', '策划',
                    '编写', '吉他', 'Studio', '制作 ', '母带', '钢琴', '贝斯', '鼓手','网易 音乐',
                    'Da', 'doo', 'ya', 'oh', 'ooh', 'la']

        if more == 'more':
            for word in self.word_pool:
                if word in useless2:
                    self.word_pool.remove(word)
        else:
            for word in self.word_pool:
                if word in useless:
                    self.word_pool.remove(word)
