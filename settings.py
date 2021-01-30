class Settings:
    # 切换按钮，如果为真，则执行爬取搜索结果的歌单，如果为假，则爬取单个歌单
    toggle = True
    # 设置搜索关键词
    search_keyword = '摇滚'
    # 设置结果限制数
    result_limit = 20

    # 设置歌单url，仅爬一张歌单时
    playlist_url = 'https://music.163.com/#/discover/toplist?id=3778678'
    playlist_title = '云音乐热歌榜'
    # 设置分词过滤强度
    more = 'e'  # 分为''、'm'去语气、'e'去英文和语气
    # 打印排名
    word_rank = True
    num = 50  # 前多少名
    csv_fname = search_keyword if toggle else playlist_title

    def __init__(self):
        pass

    def set_search_word_for_list(self, search_word):
        self.search_keyword = search_word
        self.toggle = True
        self.csv_fname = search_word
