from playwright.sync_api import sync_playwright

def test_crawler():
    """
    测试爬虫是否能正确提取百度热搜数据
    """
    try:
        print("开始测试爬虫...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 访问百度热搜实时榜单
            url = "https://top.baidu.com/board?tab=realtime"
            print(f"访问URL: {url}")
            page.goto(url, timeout=30000)
            
            # 等待页面加载完成
            print("等待页面加载完成...")
            page.wait_for_load_state('networkidle', timeout=15000)
            
            # 提取热搜数据
            print("提取热搜数据...")
            hot_search_items = page.query_selector_all('.category-wrap_iQLoo')
            
            print(f"找到 {len(hot_search_items)} 个热搜项")
            
            # 测试提取第一个项的数据
            if hot_search_items:
                first_item = hot_search_items[0]
                
                # 获取标题
                title_element = first_item.query_selector('.c-single-text-ellipsis')
                title = title_element.text_content().strip() if title_element else ""
                print(f"第一个热搜标题: {title}")
                
                # 获取链接
                url_element = first_item.query_selector('a')
                url = url_element.get_attribute('href') if url_element else ""
                if url and not url.startswith('http'):
                    url = "https://top.baidu.com" + url
                print(f"链接: {url}")
                
                # 获取图片
                image_element = first_item.query_selector('img')
                image_url = ""
                if image_element:
                    image_url = image_element.get_attribute('src')
                    if image_url and not image_url.startswith('http'):
                        image_url = "https:" + image_url
                print(f"图片URL: {image_url}")
                
                # 获取热搜指数
                hot_index_element = first_item.query_selector('.hot-index_1Bl1a')
                hot_index = hot_index_element.text_content().strip() if hot_index_element else ""
                print(f"热搜指数: {hot_index}")
            
            browser.close()
            print("测试完成")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_crawler()