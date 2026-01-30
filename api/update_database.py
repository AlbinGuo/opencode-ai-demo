import psycopg2

def update_database_schema():
    """
    修改数据库表结构，添加图片和热搜指数字段
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="demo",
            user="postgres",
            password="admin"
        )
        cur = conn.cursor()
        
        # 检查字段是否存在
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'baidu_hot_search' AND column_name = 'image_url'")
        image_column_exists = cur.fetchone() is not None
        
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'baidu_hot_search' AND column_name = 'hot_index'")
        hot_index_column_exists = cur.fetchone() is not None
        
        # 添加字段
        if not image_column_exists:
            cur.execute("ALTER TABLE baidu_hot_search ADD COLUMN image_url TEXT")
            print("添加了 image_url 字段")
        
        if not hot_index_column_exists:
            cur.execute("ALTER TABLE baidu_hot_search ADD COLUMN hot_index TEXT")
            print("添加了 hot_index 字段")
        
        conn.commit()
        cur.close()
        conn.close()
        print("数据库表结构更新完成")
        
    except Exception as e:
        print(f"更新数据库表结构失败: {e}")

if __name__ == "__main__":
    update_database_schema()
