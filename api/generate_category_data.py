import psycopg2
from datetime import datetime

def generate_category_data():
    """
    生成三个分类的百度热搜测试数据
    """
    try:
        # 连接数据库
        conn = psycopg2.connect(
            host="localhost",
            database="demo",
            user="postgres",
            password="admin"
        )
        cur = conn.cursor()
        
        # 清空现有数据
        cur.execute("DELETE FROM baidu_hot_search")
        print("已清空现有数据")
        
        # 生成三个分类的测试数据
        categories = [
            {
                "name": "realtime",
                "display_name": "热搜",
                "items": [
                    {"rank": 1, "title": "冰天雪地也是金山银山", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img1.jpg", "hot_index": "7904144"},
                    {"rank": 2, "title": "国防部回应日本可能'强登钓鱼岛'", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img2.jpg", "hot_index": "7808823"},
                    {"rank": 3, "title": "宝可梦踩靖国神社红线不是初犯", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img3.jpg", "hot_index": "7714377"},
                    {"rank": 4, "title": "震撼！'陆地航母'高铁蓄势待发", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img4.jpg", "hot_index": "7617338"},
                    {"rank": 5, "title": "这3种运动堪称'心血管保镖'", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img5.jpg", "hot_index": "7521693"}
                ]
            },
            {
                "name": "movie",
                "display_name": "电影",
                "items": [
                    {"rank": 1, "title": "春节档电影票房创新高", "url": "https://top.baidu.com/board?tab=movie", "image_url": "https://img.baidu.com/movie1.jpg", "hot_index": "6500000"},
                    {"rank": 2, "title": "《阿凡达3》全球首映", "url": "https://top.baidu.com/board?tab=movie", "image_url": "https://img.baidu.com/movie2.jpg", "hot_index": "6400000"},
                    {"rank": 3, "title": "国产科幻电影新突破", "url": "https://top.baidu.com/board?tab=movie", "image_url": "https://img.baidu.com/movie3.jpg", "hot_index": "6300000"},
                    {"rank": 4, "title": "电影节获奖名单揭晓", "url": "https://top.baidu.com/board?tab=movie", "image_url": "https://img.baidu.com/movie4.jpg", "hot_index": "6200000"},
                    {"rank": 5, "title": "经典电影重映受热捧", "url": "https://top.baidu.com/board?tab=movie", "image_url": "https://img.baidu.com/movie5.jpg", "hot_index": "6100000"}
                ]
            },
            {
                "name": "sport",
                "display_name": "体育",
                "items": [
                    {"rank": 1, "title": "国足世预赛首战告捷", "url": "https://top.baidu.com/board?tab=sport", "image_url": "https://img.baidu.com/sport1.jpg", "hot_index": "5500000"},
                    {"rank": 2, "title": "NBA全明星赛阵容公布", "url": "https://top.baidu.com/board?tab=sport", "image_url": "https://img.baidu.com/sport2.jpg", "hot_index": "5400000"},
                    {"rank": 3, "title": "冬奥会倒计时100天", "url": "https://top.baidu.com/board?tab=sport", "image_url": "https://img.baidu.com/sport3.jpg", "hot_index": "5300000"},
                    {"rank": 4, "title": "中超联赛精彩瞬间", "url": "https://top.baidu.com/board?tab=sport", "image_url": "https://img.baidu.com/sport4.jpg", "hot_index": "5200000"},
                    {"rank": 5, "title": "体育明星跨界综艺", "url": "https://top.baidu.com/board?tab=sport", "image_url": "https://img.baidu.com/sport5.jpg", "hot_index": "5100000"}
                ]
            }
        ]
        
        # 插入测试数据
        total_inserted = 0
        for category in categories:
            for item in category["items"]:
                cur.execute(
                    "INSERT INTO baidu_hot_search (title, url, image_url, hot_index, rank_num, category, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (item["title"], item["url"], item["image_url"], item["hot_index"], item["rank"], category["name"], datetime.now())
                )
                total_inserted += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"成功插入 {total_inserted} 条测试数据，涵盖 {len(categories)} 个分类")
        
    except Exception as e:
        print(f"生成测试数据失败: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    generate_category_data()