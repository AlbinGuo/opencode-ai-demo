import psycopg2
from datetime import datetime

def generate_test_data():
    """
    生成测试数据并插入到数据库中
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
        
        # 生成测试数据
        test_data = [
            {
                "rank": 1,
                "title": "冰天雪地也是金山银山",
                "url": "https://top.baidu.com/board?tab=realtime",
                "image_url": "https://img.baidu.com/img.jpg",
                "hot_index": "7904144"
            },
            {
                "rank": 2,
                "title": "国防部回应日本可能'强登钓鱼岛'",
                "url": "https://top.baidu.com/board?tab=realtime",
                "image_url": "https://img.baidu.com/img2.jpg",
                "hot_index": "7808823"
            },
            {
                "rank": 3,
                "title": "宝可梦踩靖国神社红线不是初犯",
                "url": "https://top.baidu.com/board?tab=realtime",
                "image_url": "https://img.baidu.com/img3.jpg",
                "hot_index": "7714377"
            },
            {
                "rank": 4,
                "title": "震撼！'陆地航母'高铁蓄势待发",
                "url": "https://top.baidu.com/board?tab=realtime",
                "image_url": "https://img.baidu.com/img4.jpg",
                "hot_index": "7617338"
            },
            {
                "rank": 5,
                "title": "这3种运动堪称'心血管保镖'",
                "url": "https://top.baidu.com/board?tab=realtime",
                "image_url": "https://img.baidu.com/img5.jpg",
                "hot_index": "7521693"
            }
        ]
        
        # 插入测试数据
        for item in test_data:
            cur.execute(
                "INSERT INTO baidu_hot_search (title, url, image_url, hot_index, rank_num, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                (item["title"], item["url"], item["image_url"], item["hot_index"], item["rank"], datetime.now())
            )
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"成功插入 {len(test_data)} 条测试数据")
        
    except Exception as e:
        print(f"生成测试数据失败: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    generate_test_data()