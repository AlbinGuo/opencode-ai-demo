"""
Vercel Serverless FastAPI App
用于Vercel部署的入口文件
"""
from main import app

# Vercel serverless handler
handler = app
