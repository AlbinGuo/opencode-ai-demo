import psycopg2

def add_category_column():
    """
    向baidu_hot_search表添加分类字段
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
        
        # 检查category字段是否存在
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'baidu_hot_search' AND column_name = 'category'")
        column_exists = cur.fetchone() is not None
        
        if not column_exists:
            # 添加category字段
            cur.execute("ALTER TABLE baidu_hot_search ADD COLUMN category TEXT DEFAULT 'realtime'")
            conn.commit()
            print("成功添加category字段到baidu_hot_search表")
        else:
            print("category字段已存在，跳过添加步骤")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"修改数据库架构失败: {e}")

if __name__ == "__main__":
    add_category_column()