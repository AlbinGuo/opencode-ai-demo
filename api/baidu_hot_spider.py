"""
百度热搜爬虫模块
用于获取百度热搜榜的实时数据
"""
import requests
import re
import json
from typing import List, Dict, Any


class BaiduHotSearchSpider:
    """百度热搜爬虫"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_hot_search(self, category: str = "realtime") -> List[Dict[str, Any]]:
        """
        获取百度热搜数据

        Args:
            category: 分类，可选值：realtime(实时), movie(电影), sport(体育), tech(科技), entertainment(娱乐)

        Returns:
            热搜数据列表
        """
        try:
            url = f"https://top.baidu.com/board?tab={category}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            text = self._decode_response(response.content)
            data = self._parse_response(text, category)
            return data
        except Exception as e:
            print(f"获取百度热搜{category}失败: {e}")
            return []

    def _decode_response(self, content: bytes) -> str:
        """解码响应内容"""
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
        for enc in encodings:
            try:
                return content.decode(enc, errors='ignore')
            except:
                continue
        return content.decode('utf-8', errors='ignore')

    def _parse_response(self, html: str, category: str) -> List[Dict[str, Any]]:
        """解析HTML响应，提取热搜数据"""
        results = []

        try:
            words = re.findall(r'"word":"([^"]+)"', html)
            descs = re.findall(r'"desc":"([^"]*)"', html)
            hot_scores = re.findall(r'"hotScore":"?(\d+)"?', html)
            urls = re.findall(r'"url":"(https?://[^"]+)"', html)
            imgs = re.findall(r'"img":"(https?://[^"]+)"', html)

            min_len = min(len(words), 50)
            for i in range(min_len):
                results.append({
                    "word": words[i] if i < len(words) else "",
                    "desc": descs[i] if i < len(descs) else "",
                    "hot_score": hot_scores[i] if i < len(hot_scores) else "",
                    "url": urls[i] if i < len(urls) else "",
                    "img": imgs[i] if i < len(imgs) else "",
                    "index": i + 1,
                    "is_top": i < 3
                })
        except Exception as e:
            print(f"解析HTML失败: {e}")

        return results


def get_baidu_hot_search(category: str = "realtime") -> List[Dict[str, Any]]:
    """
    获取百度热搜数据

    Args:
        category: 分类，可选值：realtime(实时), movie(电影), sport(体育), tech(科技), entertainment(娱乐)

    Returns:
        热搜数据列表
    """
    spider = BaiduHotSearchSpider()
    return spider.get_hot_search(category)


if __name__ == "__main__":
    spider = BaiduHotSearchSpider()
    for cat in ['realtime', 'movie', 'sport', 'tech', 'entertainment']:
        print(f"\n=== {cat.upper()} ===")
        data = spider.get_hot_search(cat)
        print(f"Got {len(data)} items")
        for i, item in enumerate(data[:5], 1):
            print(f"{i}. {item['word']}")
