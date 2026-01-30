from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from typing import List, Dict, Any
from datetime import datetime

# 创建FastAPI应用
app = FastAPI(
    title="百度热搜API",
    description="提供百度热搜榜数据的API接口",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库连接函数
def get_db_connection():
    """
    连接到PostgreSQL数据库
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="demo",
            user="postgres",
            password="admin"
        )
        return conn
    except Exception as e:
        print(f"数据库连接错误: {e}")
        return None

# 根路径
@app.get("/")
def read_root():
    return {
        "message": "百度热搜API",
        "endpoints": {
            "hot_search": "/api/hot-search",
            "hot_search_by_rank": "/api/hot-search/{rank}"
        }
    }

# 获取所有热搜数据（支持分页和分类）
@app.get("/api/hot-search")
def get_hot_search(page: int = 1, page_size: int = 20, category: str = None):
    """
    获取百度热搜数据（支持分页和分类）
    
    Args:
        page: 页码，默认为1
        page_size: 每页数量，默认为20
        category: 分类，可选值：realtime(热搜), movie(电影), sport(体育)
    """
    conn = get_db_connection()
    if not conn:
        return {"error": "数据库连接失败"}
    
    try:
        cur = conn.cursor()
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 查询总数
        if category:
            cur.execute("SELECT COUNT(*) FROM baidu_hot_search WHERE category = %s", (category,))
        else:
            cur.execute("SELECT COUNT(*) FROM baidu_hot_search")
        total = cur.fetchone()[0]
        
        # 查询分页数据
        if category:
            cur.execute(
                "SELECT id, rank_num, title, url, created_at, image_url, hot_index, category FROM baidu_hot_search WHERE category = %s ORDER BY rank_num LIMIT %s OFFSET %s",
                (category, page_size, offset)
            )
        else:
            cur.execute(
                "SELECT id, rank_num, title, url, created_at, image_url, hot_index, category FROM baidu_hot_search ORDER BY rank_num LIMIT %s OFFSET %s",
                (page_size, offset)
            )
        
        results = cur.fetchall()
        cur.close()
        conn.close()
        
        # 格式化数据
        hot_search_data = []
        for row in results:
            # 确保row包含所有字段
            if len(row) >= 8:
                hot_search_data.append({
                    "id": row[0],
                    "rank": row[1],
                    "title": row[2],
                    "url": row[3],
                    "image_url": row[5],
                    "hot_index": row[6],
                    "category": row[7],
                    "created_at": row[4].isoformat() if isinstance(row[4], datetime) else row[4]
                })
            else:
                # 兼容旧数据结构
                hot_search_data.append({
                    "id": row[0],
                    "rank": row[1],
                    "title": row[2],
                    "url": row[3],
                    "image_url": "",
                    "hot_index": "",
                    "category": "realtime",
                    "created_at": row[4].isoformat() if isinstance(row[4], datetime) else row[4]
                })
        
        # 返回带分页信息的数据
        return {
            "data": hot_search_data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    except Exception as e:
        print(f"查询数据错误: {e}")
        return {"error": "查询数据失败"}

# 根据排名获取热搜数据
@app.get("/api/hot-search/{rank}", response_model=Dict[str, Any])
def get_hot_search_by_rank(rank: int):
    """
    根据排名获取百度热搜数据
    """
    conn = get_db_connection()
    if not conn:
        return {"error": "数据库连接失败"}
    
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, rank_num, title, url, created_at, image_url, hot_index FROM baidu_hot_search WHERE rank_num = %s",
            (rank,)
        )
        
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if not result:
            return {"error": f"未找到排名为 {rank} 的热搜数据"}
        
        # 格式化数据
        hot_search_item = {
            "id": result[0],
            "rank": result[1],
            "title": result[2],
            "url": result[3],
            "image_url": result[5] if len(result) >= 6 else "",
            "hot_index": result[6] if len(result) >= 7 else "",
            "created_at": result[4].isoformat() if isinstance(result[4], datetime) else result[4]
        }
        
        return hot_search_item
    except Exception as e:
        print(f"查询数据错误: {e}")
        return {"error": "查询数据失败"}

# 健康检查
@app.get("/health")
def health_check():
    """
    健康检查
    """
    conn = get_db_connection()
    if conn:
        conn.close()
        return {"status": "healthy", "database": "connected"}
    else:
        return {"status": "unhealthy", "database": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
