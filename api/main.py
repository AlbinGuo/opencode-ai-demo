from fastapi import FastAPI, Depends, HTTPException, status, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, HTMLResponse
import psycopg2
import requests
from urllib.parse import urlencode
from typing import List, Dict, Any, Optional
from datetime import datetime
from auth import (
    verify_password, get_password_hash, create_access_token, decode_token,
    Token, TokenData, User, UserCreate, UserLogin
)
from pydantic import BaseModel
from gitee_config import (
    GITEE_CLIENT_ID, GITEE_CLIENT_SECRET, GITEE_REDIRECT_URI,
    GITEE_AUTH_URL, GITEE_TOKEN_URL, GITEE_USER_API
)
from db_config import get_connection_params, is_production
import os

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
from baidu_hot_spider import get_baidu_hot_search as get_baidu_hot_search_live

_cached_hot_search = []
_cached_time = 0
CACHE_DURATION = 300

def get_cached_hot_search():
    """获取缓存的实时热搜数据"""
    global _cached_hot_search, _cached_time
    import time
    current_time = time.time()
    
    if not _cached_hot_search or (current_time - _cached_time) > CACHE_DURATION:
        try:
            _cached_hot_search = get_baidu_hot_search_live("realtime")
            _cached_time = current_time
            print(f"刷新百度热搜缓存，共 {_cached_hot_search} 条数据")
        except Exception as e:
            print(f"获取百度热搜失败: {e}")
    
    return _cached_hot_search

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# 创建FastAPI应用
app = FastAPI(
    title="百度热搜API",
    description="提供百度热搜榜数据的API接口",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3006",
        "https://*.vercel.app",
        "https://*.railway.app"
    ] if is_production() else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """连接到PostgreSQL数据库"""
    try:
        conn = psycopg2.connect(**get_connection_params())
        return conn
    except Exception as e:
        print(f"数据库连接错误: {e}")
        return None

def get_user_by_username(username: str) -> Optional[Dict]:
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, password_hash, gitee_username, avatar_url, created_at FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "password_hash": user[3],
                "gitee_username": user[4],
                "avatar_url": user[5],
                "created_at": user[6]
            }
        return None
    except Exception as e:
        print(f"查询用户错误: {e}")
        return None

def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, gitee_username, avatar_url, created_at FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "gitee_username": user[3],
                "avatar_url": user[4],
                "created_at": user[5]
            }
        return None
    except Exception as e:
        print(f"查询用户错误: {e}")
        return None

def create_user(user: UserCreate) -> Optional[Dict]:
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        hashed_password = get_password_hash(user.password)
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id, username, email, created_at",
            (user.username, user.email, hashed_password)
        )
        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {
            "id": new_user[0],
            "username": new_user[1],
            "email": new_user[2],
            "created_at": new_user[3]
        }
    except psycopg2.IntegrityError:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    except Exception as e:
        print(f"创建用户错误: {e}")
        return None

def get_user_by_gitee_id(gitee_id: str) -> Optional[Dict]:
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, gitee_id, created_at FROM users WHERE gitee_id = %s", (gitee_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "gitee_id": user[3],
                "created_at": user[4]
            }
        return None
    except Exception as e:
        print(f"查询用户错误: {e}")
        return None

def get_user_by_email(email: str) -> Optional[Dict]:
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, password_hash, gitee_id, created_at FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "password_hash": user[3],
                "gitee_id": user[4],
                "created_at": user[5]
            }
        return None
    except Exception as e:
        print(f"查询用户错误: {e}")
        return None

def create_or_link_gitee_user(gitee_id: str, username: str, email: str, gitee_username: str = None, avatar_url: str = None) -> Dict:
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    print(f"[DEBUG] create_or_link_gitee_user: gitee_id={gitee_id}, username={username}, email={email}")
    print(f"[DEBUG] gitee_username={gitee_username}, avatar_url={avatar_url}")
    
    try:
        cur = conn.cursor()
        
        cur.execute("SELECT id, username, email, gitee_username, avatar_url FROM users WHERE gitee_id = %s", (gitee_id,))
        existing_user = cur.fetchone()
        
        print(f"[DEBUG] existing_user: {existing_user}")
        
        if existing_user:
            cur.execute(
                "UPDATE users SET gitee_username = %s, avatar_url = %s WHERE gitee_id = %s RETURNING id, username, email, gitee_username, avatar_url",
                (gitee_username, avatar_url, gitee_id)
            )
            updated = cur.fetchone()
            conn.commit()
            print(f"[DEBUG] Updated user: {updated}")
            cur.close()
            conn.close()
            return {
                "id": updated[0],
                "username": updated[1],
                "email": updated[2],
                "gitee_username": updated[3],
                "avatar_url": updated[4]
            }
        
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_email = cur.fetchone()
        
        if existing_email:
            cur.execute(
                "UPDATE users SET gitee_id = %s, gitee_username = %s, avatar_url = %s WHERE id = %s RETURNING id, username, email, gitee_username, avatar_url",
                (gitee_id, gitee_username, avatar_url, existing_email[0])
            )
            updated_user = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return {
                "id": updated_user[0],
                "username": updated_user[1],
                "email": updated_user[2],
                "gitee_username": updated_user[3],
                "avatar_url": updated_user[4]
            }
        
        cur.execute(
            "INSERT INTO users (username, email, gitee_id, gitee_username, avatar_url, password_hash) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, username, email, gitee_username, avatar_url",
            (username, email, gitee_id, gitee_username, avatar_url, get_password_hash(gitee_id))
        )
        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {
            "id": new_user[0],
            "username": new_user[1],
            "email": new_user[2],
            "gitee_username": new_user[3],
            "avatar_url": new_user[4]
        }
    except Exception as e:
        print(f"创建/绑定 Gitee 用户错误: {e}")
        raise HTTPException(status_code=500, detail="处理用户信息失败")

# 根路径
@app.get("/")
def read_root():
    return {
        "message": "百度热搜API",
        "endpoints": {
            "hot_search": "/api/hot-search",
            "hot_search_by_rank": "/api/hot-search/{rank}",
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login",
                "me": "/api/auth/me"
            }
        }
    }

@app.post("/api/auth/register", response_model=User)
def register(user: UserCreate):
    """
    用户注册
    """
    existing_user = get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    new_user = create_user(user)
    if not new_user:
        raise HTTPException(status_code=500, detail="创建用户失败")
    return new_user

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录
    """
    user = get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"], "user_id": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    获取当前登录用户信息
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_token(token)
    if token_data is None:
        raise credentials_exception
    user = get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "gitee_id": user.get("gitee_id"),
        "gitee_username": user.get("gitee_username"),
        "avatar_url": user.get("avatar_url"),
        "created_at": user["created_at"]
    }

@app.get("/api/auth/gitee")
def gitee_login():
    """
    Gitee 登录入口，重定向到 Gitee 授权页面
    """
    if not GITEE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Gitee Client ID 未配置")
    
    params = {
        "client_id": GITEE_CLIENT_ID,
        "redirect_uri": GITEE_REDIRECT_URI,
        "response_type": "code",
        "scope": "user_info emails"
    }
    auth_url = f"{GITEE_AUTH_URL}?{urlencode(params)}"
    return {"auth_url": auth_url}

@app.get("/auth/gitee/callback")
async def gitee_callback(code: str = Query(...)):
    """
    Gitee OAuth2 回调接口
    """
    if not GITEE_CLIENT_ID or not GITEE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Gitee 配置不完整")
    
    try:
        token_response = requests.post(GITEE_TOKEN_URL, data={
            "grant_type": "authorization_code",
            "client_id": GITEE_CLIENT_ID,
            "client_secret": GITEE_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITEE_REDIRECT_URI
        })
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="获取 access_token 失败")
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        print(f"[DEBUG] token_data: {token_data}")
        
        gitee_user = {}
        email = None
        
        print(f"[DEBUG] 正在请求 Gitee 用户 API...")
        user_response = requests.get(GITEE_USER_API, params={
            "access_token": access_token
        })
        
        print(f"[DEBUG] user_response status: {user_response.status_code}")
        
        if user_response.status_code == 200:
            gitee_user = user_response.json()
            email = gitee_user.get("email")
            print(f"[DEBUG] ========== Gitee 用户完整数据 ==========")
            import json
            print(json.dumps(gitee_user, indent=2, ensure_ascii=False))
            print(f"[DEBUG] ============================================")
        
        if not email:
            emails_response = requests.get("https://gitee.com/api/v5/user/emails", params={
                "access_token": access_token
            })
            if emails_response.status_code == 200:
                emails = emails_response.json()
                for e in emails:
                    if e.get("email") and e.get("primary"):
                        email = e.get("email")
                        break
                if not email and emails and len(emails) > 0:
                    email = emails[0].get("email")
        
        if not email:
            raise HTTPException(status_code=400, detail="无法获取用户邮箱，请在 Gitee 授权邮箱权限")
        
        gitee_id = str(gitee_user.get("id")) if gitee_user else "unknown"
        username = gitee_user.get("login") or gitee_user.get("name") or f"gitee_user_{gitee_id}"
        gitee_username = gitee_user.get("name")
        avatar_url = gitee_user.get("avatar_url")
        
        print(f"[DEBUG] Final values: gitee_id={gitee_id}, username={username}, email={email}")
        print(f"[DEBUG] gitee_username={gitee_username}, avatar_url={avatar_url}")
        
        user = create_or_link_gitee_user(gitee_id, username, email, gitee_username, avatar_url)
        
        jwt_token = create_access_token(data={"sub": user["username"], "user_id": user["id"]})
        
        frontend_url = FRONTEND_URL
        redirect_url = f"{frontend_url}/login?token={jwt_token}&avatar={avatar_url or ''}"
        
        return RedirectResponse(url=redirect_url)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Gitee 登录错误: {e}")
        raise HTTPException(status_code=500, detail="Gitee 登录失败")

# 城市代码映射
CITY_CODE_MAP = {
    "101200300": "西安",
    "101010100": "北京",
    "101020100": "上海",
    "101280100": "广州",
    "101280600": "深圳",
    "101210100": "杭州",
    "101230200": "成都",
    "101200100": "武汉",
    "101190400": "南京"
}
from jobs_spider import BossZhipinSpider, get_foreign_jobs_sample, get_jobs_from_db, crawl_and_save_jobs

@app.get("/api/jobs")
def get_jobs(
    query: str = None,
    city: str = None,
    page: int = 1,
    page_size: int = 10
):
    """
    从数据库获取招聘列表
    
    Args:
        query: 搜索关键词
        city: 城市代码
        page: 页码
        page_size: 每页数量
    """
    try:
        city_name = CITY_CODE_MAP.get(city, city)
        result = get_jobs_from_db(
            query=query,
            city=city_name,
            page=page,
            page_size=page_size
        )
        return result
    except Exception as e:
        print(f"获取招聘信息错误: {e}")
        return {"error": "获取招聘信息失败", "data": [], "total": 0}

@app.get("/api/jobs/{job_id}")
def get_job_detail(job_id: int):
    """
    获取单个职位详情
    
    Args:
        job_id: 职位ID
    """
    from jobs_spider import JobsDB
    db = JobsDB()
    try:
        job = db.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="职位不存在")
        return {"data": job}
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取职位详情错误: {e}")
        raise HTTPException(status_code=500, detail="获取职位详情失败")

@app.get("/api/jobs/foreign")
def get_foreign_jobs(
    query: str = "Python",
    city: str = "101200300",
    page: int = 1,
    page_size: int = 10
):
    """
    获取外企招聘信息（从数据库）
    
    Args:
        query: 搜索关键词
        city: 城市代码
        page: 页码
        page_size: 每页数量
    """
    try:
        city_name = CITY_CODE_MAP.get(city, city)
        result = get_jobs_from_db(
            query=query,
            city=city_name,
            page=page,
            page_size=page_size
        )
        return result
    except Exception as e:
        print(f"获取招聘信息错误: {e}")
        return {"error": "获取招聘信息失败", "data": [], "total": 0}

@app.post("/api/jobs/crawl")
def crawl_jobs(
    query: str = "Python",
    city: str = "101200300",
    max_pages: int = 3
):
    """
    爬取并保存招聘信息到数据库
    
    Args:
        query: 搜索关键词
        city: 城市代码
        max_pages: 最大爬取页数
    """
    try:
        result = crawl_and_save_jobs(
            query=query,
            city=city,
            max_pages=max_pages
        )
        return {
            "message": "爬取完成",
            "crawled": result["crawled"],
            "saved": result["saved"],
            "query": result["query"],
            "city": result["city"]
        }
    except Exception as e:
        print(f"爬取招聘信息错误: {e}")
        return {"error": "爬取招聘信息失败"}

@app.get("/api/jobs/stats")
def get_jobs_stats():
    """
    获取招聘数据统计
    """
    from jobs_spider import JobsDB
    db = JobsDB()
    try:
        total = db.get_jobs_count()
        return {"total_jobs": total}
    except Exception as e:
        print(f"获取统计数据错误: {e}")
        return {"error": "获取统计数据失败", "total_jobs": 0}

@app.get("/api/jobs/sample")
def get_jobs_sample():
    """获取示例招聘数据（用于开发测试）"""
    return {
        "data": get_foreign_jobs_sample(),
        "total": len(get_foreign_jobs_sample()),
        "page": 1,
        "page_size": 10
    }

@app.get("/api/jobs/cities")
def get_job_cities():
    """获取支持的城市列表"""
    return {
        "cities": [
            {"code": "101200300", "name": "西安"},
            {"code": "101010100", "name": "北京"},
            {"code": "101020100", "name": "上海"},
            {"code": "101280100", "name": "广州"},
            {"code": "101280600", "name": "深圳"},
            {"code": "101210100", "name": "杭州"},
            {"code": "101230200", "name": "成都"},
            {"code": "101200100", "name": "武汉"},
            {"code": "101190400", "name": "南京"}
        ]
    }

# 获取所有热搜数据（支持分页和分类）
@app.get("/api/hot-search")
def get_hot_search(
    page: int = Query(1),
    page_size: int = Query(20),
    category: str = Query(None)
):
    """
    获取百度热搜数据（支持分页和分类）
    
    Args:
        page: 页码，默认为1
        page_size: 每页数量，默认为20
        category: 分类，可选值：realtime(实时), movie(电影), sport(体育), tech(科技), entertainment(娱乐)
    """
    try:
        cat = category or "realtime"
        live_data = get_baidu_hot_search_live(cat)
        
        if live_data and len(live_data) > 0:
            total = len(live_data)
            offset = (page - 1) * page_size
            page_data = live_data[offset:offset + page_size]
            
            formatted_data = []
            for idx, item in enumerate(page_data, start=offset + 1):
                formatted_data.append({
                    "id": item.get("index", idx),
                    "rank": item.get("index", idx),
                    "title": item.get("word", ""),
                    "url": item.get("url", ""),
                    "image_url": item.get("img", ""),
                    "hot_index": item.get("hot_score", ""),
                    "category": category or "realtime",
                    "created_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                })
            
            return {
                "data": formatted_data,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size
            }
    except Exception as e:
        print(f"获取百度热搜数据失败: {e}")
    
    return {"data": [], "total": 0, "page": page, "page_size": page_size, "total_pages": 0}

# 根据排名获取热搜数据
@app.get("/api/hot-search/{rank}", response_model=Dict[str, Any])
def get_hot_search_by_rank(rank: int):
    """
    根据排名获取百度热搜数据
    """
    hot_list = get_cached_hot_search()
    
    if rank >= 1 and rank <= len(hot_list):
        item = hot_list[rank - 1]
        return {
            "id": item.get("index", rank),
            "rank": item.get("index", rank),
            "title": item.get("word", ""),
            "url": item.get("url", ""),
            "image_url": item.get("img", ""),
            "hot_index": item.get("hot_score", ""),
            "category": "realtime",
            "created_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, rank_num, title, url, created_at, image_url, hot_index, category FROM baidu_hot_search WHERE rank_num = %s ORDER BY created_at DESC LIMIT 1",
                (rank,)
            )
            row = cur.fetchone()
            cur.close()
            conn.close()
            
            if row:
                return {
                    "id": row[0],
                    "rank": row[1],
                    "title": row[2],
                    "url": row[3],
                    "image_url": row[5] or "",
                    "hot_index": row[6] or "",
                    "category": row[7] or "realtime",
                    "created_at": row[4].isoformat() if hasattr(row[4], 'isoformat') else str(row[4])
                }
        except Exception as e:
            print(f"数据库查询错误: {e}")
    
    return {"error": f"未找到排名为 {rank} 的热搜数据"}

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
    uvicorn.run(app, host="0.0.0.0", port=8002)
