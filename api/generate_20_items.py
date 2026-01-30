import psycopg2
from datetime import datetime

def generate_20_items():
    """
    生成20条百度热搜测试数据
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
        
        # 生成20条测试数据
        test_data = [
            {"rank": 1, "title": "冰天雪地也是金山银山", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img1.jpg", "hot_index": "7904144"},
            {"rank": 2, "title": "国防部回应日本可能'强登钓鱼岛'", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img2.jpg", "hot_index": "7808823"},
            {"rank": 3, "title": "宝可梦踩靖国神社红线不是初犯", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img3.jpg", "hot_index": "7714377"},
            {"rank": 4, "title": "震撼！'陆地航母'高铁蓄势待发", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img4.jpg", "hot_index": "7617338"},
            {"rank": 5, "title": "这3种运动堪称'心血管保镖'", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img5.jpg", "hot_index": "7521693"},
            {"rank": 6, "title": "'自制霉豆腐'火了", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img6.jpg", "hot_index": "7424755"},
            {"rank": 7, "title": "开年首月 中央纪委打7虎", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img7.jpg", "hot_index": "7327809"},
            {"rank": 8, "title": "华为手机全系降价 最高降4000元", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img8.jpg", "hot_index": "7237119"},
            {"rank": 9, "title": "'一家人给自己盖了个小区'", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img9.jpg", "hot_index": "7136229"},
            {"rank": 10, "title": "邻居楼道放鞋架 女子挂婆婆遗照反击", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img10.jpg", "hot_index": "7045271"},
            {"rank": 11, "title": "一家人吃自制牛瘪火锅中毒双手变蓝", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img11.jpg", "hot_index": "6951781"},
            {"rank": 12, "title": "人工智能发展新突破", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img12.jpg", "hot_index": "6850000"},
            {"rank": 13, "title": "全球气候变化会议", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img13.jpg", "hot_index": "6750000"},
            {"rank": 14, "title": "新能源汽车销量创新高", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img14.jpg", "hot_index": "6650000"},
            {"rank": 15, "title": "教育改革新政策", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img15.jpg", "hot_index": "6550000"},
            {"rank": 16, "title": "科技创新成果展示", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img16.jpg", "hot_index": "6450000"},
            {"rank": 17, "title": "医疗健康新研究", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img17.jpg", "hot_index": "6350000"},
            {"rank": 18, "title": "航天事业新进展", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img18.jpg", "hot_index": "6250000"},
            {"rank": 19, "title": "体育赛事精彩瞬间", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img19.jpg", "hot_index": "6150000"},
            {"rank": 20, "title": "文化遗产保护", "url": "https://top.baidu.com/board?tab=realtime", "image_url": "https://img.baidu.com/img20.jpg", "hot_index": "6050000"}
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
    generate_20_items()