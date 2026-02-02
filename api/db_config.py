"""
数据库配置模块
统一管理数据库连接配置，支持环境变量覆盖
"""
import os
from typing import Optional

def get_db_config() -> dict:
    """
    获取数据库配置
    优先使用环境变量，其次使用默认值
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "demo"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "admin")
    }


def get_database_url() -> str:
    """
    获取DATABASE_URL格式的连接字符串
    兼容Railway等云服务
    """
    database_url = os.getenv("DATABASE_URL", "")
    if database_url:
        return database_url
    
    config = get_db_config()
    return f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"


def get_connection_params() -> dict:
    """
    获取psycopg2连接参数
    """
    database_url = os.getenv("DATABASE_URL", "")
    
    if database_url:
        return {"dsn": database_url}
    
    config = get_db_config()
    return {
        "host": config["host"],
        "port": config["port"],
        "database": config["database"],
        "user": config["user"],
        "password": config["password"]
    }


def is_production() -> bool:
    """判断是否为生产环境"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    return env == "production"
