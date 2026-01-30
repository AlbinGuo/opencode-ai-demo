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
        }
    
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
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = self._parse_response(response.text)
            return data
        except Exception as e:
            print(f"获取百度热搜失败: {e}")
            return []
    
    def _parse_response(self, html: str) -> List[Dict[str, Any]]:
        """解析HTML响应，提取热搜数据"""
        results = []
        
        try:
            start_idx = html.find('"cards":[{')
            if start_idx == -1:
                return results
            
            brace_count = 0
            start_brace = -1
            end_idx = -1
            
            for i in range(start_idx, len(html)):
                if html[i] == '{':
                    if start_brace == -1:
                        start_brace = i
                    brace_count += 1
                elif html[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            
            if start_brace != -1 and end_idx != -1:
                cards_json = '{"cards":[' + html[start_brace:end_idx] + ']}'
                data = json.loads(cards_json)
                results = self._extract_data(data)
        
        except Exception as e:
            print(f"解析HTML失败: {e}")
        
        return results
    
    def _extract_data(self, data: Dict) -> List[Dict[str, Any]]:
        """从解析的数据中提取热搜列表"""
        results = []
        
        try:
            if 'cards' in data:
                for card in data['cards']:
                    if card.get('component') == 'hotList' and 'content' in card:
                        for idx, item in enumerate(card['content'], 1):
                            results.append({
                                "word": item.get('word', ''),
                                "desc": item.get('desc', ''),
                                "hot_score": item.get('hotScore', ''),
                                "url": item.get('url', ''),
                                "img": item.get('img', ''),
                                "index": idx,
                                "is_top": item.get('isTop', False)
                            })
                        break
        except Exception as e:
            print(f"提取数据失败: {e}")
        
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
    data = spider.get_hot_search("realtime")
    for i, item in enumerate(data[:10], 1):
        print(f"{i}. {item['word']} - {item['hot_score']}")
