import psycopg2
from datetime import datetime

"""
为热搜、电影、体育三个分类生成30条数据并存储到数据库
"""

def insert_hot_search_data(data):
    """
    将热搜数据插入到数据库
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="demo",
            user="postgres",
            password="admin"
        )
        cur = conn.cursor()
        
        # 清空现有数据
        cur.execute("DELETE FROM baidu_hot_search")
        
        # 插入新数据
        for item in data:
            cur.execute(
                "INSERT INTO baidu_hot_search (title, url, image_url, hot_index, rank_num, category, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (item["title"], item["url"], item.get("image_url", ""), item.get("hot_index", ""), item["rank"], item.get("category", "realtime"), datetime.now())
            )
        
        conn.commit()
        cur.close()
        print(f"成功插入 {len(data)} 条热搜数据")
        
    except Exception as e:
        print(f"插入数据失败: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def main():
    """
    主函数
    """
    print("为热搜、电影、体育三个分类生成30条数据...")
    
    # 为每个分类生成30条数据
    all_data = []
    
    # 热搜分类数据
    realtime_data = [
        "人工智能发展新突破", "全球气候变化会议", "新能源汽车销量创新高", "教育改革新政策", "科技创新成果展示",
        "医疗健康新研究", "航天事业新进展", "体育赛事精彩瞬间", "文化遗产保护", "经济发展新动态",
        "环境保护措施", "社会保障体系完善", "数字经济发展", "乡村振兴战略", "国际合作新机遇",
        "文化交流活动", "科技企业创新", "民生工程建设", "法律法规完善", "文化产业发展",
        "科技创新应用", "健康生活方式", "教育公平推进", "就业创业支持", "乡村旅游发展",
        "文化自信提升", "绿色发展理念", "智慧城市建设", "区域协调发展", "社会治理创新"
    ]
    
    # 电影分类数据
    movie_data = [
        "最新电影上映", "电影票房排行榜", "奥斯卡获奖影片", "国产电影佳作", "好莱坞大片",
        "电影明星动态", "电影拍摄花絮", "经典电影重映", "电影奖项评选", "电影评论分析",
        "科幻电影推荐", "动作电影集锦", "喜剧电影合集", "爱情电影精选", "悬疑电影推荐",
        "动画电影佳作", "纪录片推荐", "恐怖电影合集", "战争电影精选", "历史题材电影",
        "音乐电影推荐", "传记电影精选", "家庭电影合集", "冒险电影推荐", "奇幻电影精选",
        "犯罪电影推荐", "灾难电影合集", "武侠电影精选", "西部电影推荐", "黑色幽默电影"
    ]
    
    # 体育分类数据
    sport_data = [
        "足球赛事直播", "篮球比赛结果", "乒乓球锦标赛", "羽毛球比赛", "网球公开赛",
        "田径运动会", "游泳比赛", "体操世锦赛", "跳水比赛", "排球联赛",
        "棒球比赛", "橄榄球赛事", "高尔夫球赛", "拳击比赛", "MMA赛事",
        "自行车比赛", "赛马比赛", "帆船比赛", "滑雪赛事", "冰球比赛",
        "武术比赛", "摔跤比赛", "柔道比赛", "跆拳道比赛", "击剑比赛",
        "射击比赛", "射箭比赛", "举重比赛", "体操比赛", "田径世锦赛"
    ]
    
    # 处理热搜分类
    print("\n生成热搜分类数据...")
    for i, title in enumerate(realtime_data, 1):
        all_data.append({
            "rank": i,
            "title": title,
            "url": f"https://www.baidu.com/s?wd={title}",
            "image_url": "",
            "hot_index": str(7000000 - (i * 10000)),
            "category": "realtime"
        })
    print(f"热搜分类生成 {len(realtime_data)} 条数据")
    
    # 处理电影分类
    print("\n生成电影分类数据...")
    for i, title in enumerate(movie_data, 1):
        all_data.append({
            "rank": i,
            "title": title,
            "url": f"https://www.baidu.com/s?wd={title}",
            "image_url": "",
            "hot_index": str(7000000 - (i * 10000)),
            "category": "movie"
        })
    print(f"电影分类生成 {len(movie_data)} 条数据")
    
    # 处理体育分类
    print("\n生成体育分类数据...")
    for i, title in enumerate(sport_data, 1):
        all_data.append({
            "rank": i,
            "title": title,
            "url": f"https://www.baidu.com/s?wd={title}",
            "image_url": "",
            "hot_index": str(7000000 - (i * 10000)),
            "category": "sport"
        })
    print(f"体育分类生成 {len(sport_data)} 条数据")
    
    # 插入数据库
    print(f"\n总计生成 {len(all_data)} 条数据")
    if all_data:
        print("插入数据到数据库...")
        insert_hot_search_data(all_data)
    else:
        print("未生成任何数据")

if __name__ == "__main__":
    main()
