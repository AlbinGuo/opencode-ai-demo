from playwright.sync_api import sync_playwright

"""
测试百度热搜页面结构
"""

def test_page_structure():
    """
    测试百度热搜页面结构
    """
    try:
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=True, timeout=60000)
            page = browser.new_page()
            
            # 设置用户代理
            page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            # 访问百度热搜页面
            print("访问百度热搜页面...")
            page.goto("https://top.baidu.com/board?tab=realtime", timeout=60000)
            print("页面访问成功")
            
            # 等待页面加载完成
            print("等待页面加载完成...")
            page.wait_for_load_state('networkidle', timeout=30000)
            print("页面加载完成")
            
            # 保存页面HTML到文件
            html_content = page.content()
            with open('baidu_hot_search.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("页面HTML已保存到 baidu_hot_search.html")
            
            # 尝试提取热搜数据
            print("\n尝试提取热搜数据...")
            
            # 尝试不同的选择器
            selectors = [
                '.category-wrap_iQLoo',  # 原始选择器
                '.c-single-text-ellipsis',  # 标题选择器
                '.hot-index_1Bl1a',  # 热搜指数选择器
                '.category-wrap_iQLoo a',  # 链接选择器
                '.category-wrap_iQLoo img'  # 图片选择器
            ]
            
            for selector in selectors:
                elements = page.query_selector_all(selector)
                print(f"选择器 '{selector}' 找到 {len(elements)} 个元素")
                
                # 打印前几个元素的内容
                if elements:
                    print(f"前3个元素:")
                    for i, element in enumerate(elements[:3]):
                        if selector == '.c-single-text-ellipsis':
                            print(f"  {i+1}. {element.text_content().strip()}")
                        elif selector == '.hot-index_1Bl1a':
                            print(f"  {i+1}. {element.text_content().strip()}")
                        elif selector.endswith('a'):
                            href = element.get_attribute('href')
                            print(f"  {i+1}. {href}")
                        elif selector.endswith('img'):
                            src = element.get_attribute('src')
                            print(f"  {i+1}. {src}")
            
            browser.close()
            print("\n页面结构测试完成")
            return True
            
    except Exception as e:
        print(f"测试页面结构时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_page_structure()
