# 百度热搜榜 (Baidu Hot Search)

一个实时展示百度热搜数据的Web应用，支持多个分类（实时、影视、体育、科技、娱乐）。

## 技术栈

- **前端**: Vue 3 + Vite + Vue Router + Axios
- **后端**: FastAPI + PostgreSQL + JWT认证 + Gitee OAuth2
- **部署**: Vercel (前端) + Railway (后端)

## 快速部署

### 1. 部署后端到 Railway

```bash
# Railway会自动从GitHub部署
# 需要配置的环境变量：
# - DATABASE_URL (自动从PostgreSQL插件注入)
# - ENVIRONMENT=production
# - FRONTEND_URL=https://your-vercel-app.vercel.app
# - GITEE_CLIENT_ID
# - GITEE_CLIENT_SECRET
# - JWT_SECRET_KEY
```

### 2. 部署前端到 Vercel

```bash
# Vercel配置：
# - Build Command: npm run build
# - Output Directory: dist
# - Root Directory: frontend
# - Environment Variable: VITE_API_URL=https://your-railway-app.railway.app
```

## 项目结构

```
vibe-coding/
├── api/                    # 后端项目
│   ├── main.py            # FastAPI主应用
│   ├── auth.py            # JWT认证
│   ├── jobs_spider.py     # 招聘爬虫
│   ├── baidu_hot_spider.py # 百度热搜爬虫
│   ├── railway.json       # Railway配置
│   └── .env.production    # 生产环境变量模板
├── frontend/              # 前端项目
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── api/           # API封装
│   │   └── router/        # 路由配置
│   ├── vercel.json        # Vercel配置
│   └── .env.production    # 生产环境变量模板
└── DEPLOY.md             # 详细部署文档
```

## API接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/hot-search` | GET | 获取热搜列表 |
| `/api/hot-search/{rank}` | GET | 获取单条热搜详情 |
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/me` | GET | 获取当前用户 |
| `/api/auth/gitee` | GET | Gitee登录入口 |
| `/auth/gitee/callback` | GET | Gitee回调 |
| `/api/jobs` | GET | 招聘列表 |
| `/health` | GET | 健康检查 |

## 本地开发

```bash
# 后端
cd api
pip install -r requirements.txt
python main.py

# 前端
cd frontend
npm install
npm run dev
```

## 许可证

MIT
