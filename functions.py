import requests
from requests.exceptions import RequestException
import re

def get_page(url):
    """获得网页"""
    # 处理链接
    url = re.sub('/#', '', url)

    # 设置头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    # 尝试获取
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
    except RequestException:
        return None


