class Settings:
    def __init__(self):

        # 切换按钮，如果为真，则执行爬取搜索结果的歌单，如果为假，则爬取单个歌单
        self.toggle = True
        # 设置搜索关键词
        self.search_keyword = '超超越越'
        # 设置结果限制数
        self.result_limit = 2

        # 设置歌单url，仅爬一张歌单时
        self.playlist_url = 'https://music.163.com/#/discover/toplist?id=3778678'
        self.playlist_title = ''

        if self.toggle == True:
            self.csv_fname = self.search_keyword
        else:
            self.csv_fname = self.playlist_title


