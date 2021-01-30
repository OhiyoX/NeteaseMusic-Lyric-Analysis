# pip install requests pandas

import requests
from requests.exceptions import RequestException
import re
import pandas


def get_page(url, params=None):
    """获得网页"""
    # 处理链接
    url = re.sub('/#', '', url)

    # 设置头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    # 尝试获取
    flag = 5
    while flag > 0:
        try:
            response = requests.get(url, headers=headers, params=params)
            print(response.url)
            if response.status_code == 200:
                flag = 0
                return response
        except RequestException:
            flag -= 1
            print('retry')
            if flag <= 0:
                return None

def is_contain_chinese(check_str):
    try:
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
    except:
        return False
