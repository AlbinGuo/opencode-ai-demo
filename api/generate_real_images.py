import psycopg2
import random

# 连接数据库
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='demo',
            user='postgres',
            password='admin'
        )
        return conn
    except Exception as e:
        print(f"数据库连接错误: {e}")
        return None

# 生成真实图片URL
def generate_real_image_url():
    # 使用picsum.photos获取随机图片
    width = 200
    height = 200
    # 生成随机seed以获取不同图片
    seed = random.randint(1, 10000)
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"

# 更新数据库中的image_url字段
def update_image_urls():
    conn = get_db_connection()
    if not conn:
        print("数据库连接失败")
        return
    
    try:
        cur = conn.cursor()
        
        # 获取所有记录
        cur.execute("SELECT id FROM baidu_hot_search")
        records = cur.fetchall()
        
        print(f"找到 {len(records)} 条记录，开始更新image_url字段...")
        
        # 为每条记录更新image_url
        for record in records:
            record_id = record[0]
            image_url = generate_real_image_url()
            
            cur.execute(
                "UPDATE baidu_hot_search SET image_url = %s WHERE id = %s",
                (image_url, record_id)
            )
            
            if record_id % 10 == 0:
                print(f"已更新 {record_id} 条记录")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("所有记录的image_url字段已更新完成！")
        
    except Exception as e:
        print(f"更新数据错误: {e}")
        conn.rollback()
        cur.close()
        conn.close()

if __name__ == "__main__":
    update_image_urls()
