import psycopg2

"""
验证数据库中数据是否正确存储
"""

def verify_data():
    """
    验证数据库中的数据
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
        
        # 查询总数据量
        cur.execute("SELECT COUNT(*) FROM baidu_hot_search")
        total_count = cur.fetchone()[0]
        print(f"数据库中总数据量: {total_count}")
        
        # 查询每个分类的数据量
        categories = ["realtime", "movie", "sport"]
        category_names = {"realtime": "热搜", "movie": "电影", "sport": "体育"}
        
        for category in categories:
            cur.execute("SELECT COUNT(*) FROM baidu_hot_search WHERE category = %s", (category,))
            count = cur.fetchone()[0]
            print(f"{category_names[category]} 分类数据量: {count}")
            
            # 检查是否为30条
            if count == 30:
                print(f"✓ {category_names[category]} 分类数据量正确（30条）")
            else:
                print(f"✗ {category_names[category]} 分类数据量错误，应为30条，实际为{count}条")
        
        # 查看前几条数据结构
        print("\n查看前5条数据结构:")
        cur.execute("SELECT * FROM baidu_hot_search LIMIT 5")
        rows = cur.fetchall()
        
        for i, row in enumerate(rows, 1):
            print(f"\n第 {i} 条数据:")
            print(f"  ID: {row[0]}")
            print(f"  排名: {row[1]}")
            print(f"  标题: {row[2]}")
            print(f"  URL: {row[3]}")
            print(f"  创建时间: {row[4]}")
            print(f"  图片URL: {row[5]}")
            print(f"  热搜指数: {row[6]}")
            print(f"  分类: {category_names.get(row[7], row[7])}")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"验证数据失败: {e}")
        return False
    finally:
        if conn:
            conn.close()

def main():
    """
    主函数
    """
    print("验证数据库中数据是否正确存储...")
    success = verify_data()
    
    if success:
        print("\n✓ 数据验证成功")
    else:
        print("\n✗ 数据验证失败")

if __name__ == "__main__":
    main()
