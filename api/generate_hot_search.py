import psycopg2
from datetime import datetime

def generate_hot_search_data():
    """
    生成100条热搜数据
    """
    hot_search_list = []
    
    # 生成100条不同的热搜话题
    categories = [
        "科技", "娱乐", "体育", "财经", "教育",
        "健康", "汽车", "房产", "旅游", "文化"
    ]
    
    topics = [
        "人工智能发展新突破", "全球气候变化会议", "新能源汽车销量创新高", "教育改革新政策", "科技创新成果展示",
        "医疗健康新研究", "航天事业新进展", "体育赛事精彩瞬间", "文化遗产保护", "经济发展新动态",
        "环境保护措施", "社会保障体系完善", "数字经济发展", "乡村振兴战略", "国际合作新机遇",
        "文化交流活动", "科技企业创新", "民生工程建设", "法律法规完善", "文化产业发展",
        "科技创新应用", "健康生活方式", "教育公平推进", "就业创业支持", "乡村旅游发展",
        "文化自信提升", "绿色发展理念", "智慧城市建设", "区域协调发展", "社会治理创新",
        "科技创新人才", "医疗卫生改革", "文化传承弘扬", "生态环境保护", "对外开放扩大",
        "数字技术应用", "健康中国行动", "教育质量提升", "乡村基础设施", "文化市场繁荣",
        "科技成果转化", "全民健身活动", "教育资源均衡", "乡村特色产业", "文化创意产业",
        "科技创新平台", "医保政策完善", "教育评价改革", "乡村环境整治", "文化交流互鉴",
        "人工智能应用", "公共卫生体系", "职业教育发展", "乡村文化振兴", "文化品牌打造",
        "量子计算研究", "医疗服务改善", "高等教育发展", "乡村人才振兴", "文化产业融合",
        "生物科技突破", "养老服务体系", "教育信息化", "乡村生态振兴", "文化自信增强",
        "新材料研发", "医药创新发展", "教育国际化", "乡村组织振兴", "文化遗产利用",
        "新能源技术", "健康产业发展", "教育改革试点", "乡村产业融合", "文化市场规范",
        "科技创新前沿", "健康生活理念", "教育创新模式", "乡村振兴成效", "文化软实力提升",
        "科技与生活", "健康医疗服务", "教育均衡发展", "乡村旅游特色", "文化创新发展",
        "科技创新驱动", "健康产业未来", "教育现代化", "乡村振兴路径", "文化传承创新"
    ]
    
    # 生成100条数据
    for i in range(1, 101):
        # 循环使用话题
        topic_index = (i - 1) % len(topics)
        category_index = (i - 1) % len(categories)
        
        # 生成标题
        if i <= 50:
            title = topics[topic_index]
        else:
            title = f"{categories[category_index]}领域热点: {topics[topic_index]}"
        
        # 生成链接
        url = f"https://www.baidu.com/s?wd={title}"
        
        hot_search_list.append({
            "rank": i,
            "title": title,
            "url": url
        })
    
    return hot_search_list

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
                "INSERT INTO baidu_hot_search (title, url, rank_num, created_at) VALUES (%s, %s, %s, %s)",
                (item["title"], item["url"], item["rank"], datetime.now())
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
    print("生成100条热搜数据...")
    hot_search_data = generate_hot_search_data()
    print(f"生成了 {len(hot_search_data)} 条热搜数据")
    
    print("插入数据到数据库...")
    insert_hot_search_data(hot_search_data)
    
    # 验证数据
    conn = psycopg2.connect(
        host="localhost",
        database="demo",
        user="postgres",
        password="admin"
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM baidu_hot_search")
    count = cur.fetchone()[0]
    print(f"数据库中现有 {count} 条数据")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
