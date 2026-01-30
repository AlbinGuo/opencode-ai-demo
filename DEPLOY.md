# 部署指南

## 项目结构

```
baidu-hot-search/
├── api/                    # 后端 (FastAPI + PostgreSQL)
│   ├── main.py            # 主应用
│   ├── auth.py            # 认证模块
│   ├── jobs_spider.py     # 招聘爬虫
│   └── baidu_hot_spider.py # 百度热搜爬虫
├── frontend/              # 前端 (Vue 3 + Vite)
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   └── api/           # API封装
│   └── dist/              # 构建产物
└── vercel.json           # Vercel配置
```

## 部署方式

### 方式一：Vercel部署前端 + Railway/Render部署后端（推荐）

#### 1. 部署后端（Railway）

1. 访问 [Railway](https://railway.app) 并登录
2. 点击 "New Project" → "Deploy from GitHub"
3. 选择本仓库
4. 添加环境变量：
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   GITEE_CLIENT_ID=your_gitee_client_id
   GITEE_CLIENT_SECRET=your_gitee_client_secret
   ```
5. 部署完成后获取后端URL，如：`https://your-app.railway.app`

#### 2. 部署前端（Vercel）

1. 访问 [Vercel](https://vercel.com) 并登录
2. 点击 "Add New..." → "Project"
3. 导入本仓库
4. 配置构建命令：
   ```
   Build Command: cd frontend && npm run build
   Output Directory: frontend/dist
   ```
5. 添加环境变量：
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```
6. 点击 "Deploy"

#### 3. 更新Gitee回调地址

在Gitee开发者设置中更新回调地址：
```
https://your-vercel-frontend.vercel.app/auth/gitee/callback
```

### 方式二：Vercel Serverless Functions

Vercel支持Python Serverless Functions，但需要注意：
- 数据库连接需要在函数内创建
- 每次调用会冷启动
- 有执行时间限制（10秒）

```bash
# 本地测试Vercel Serverless Functions
npm i -g vercel
vercel dev
```

## 本地开发

### 后端
```bash
cd api
pip install -r requirements.txt
python main.py
# 运行在 http://localhost:8002
```

### 前端
```bash
cd frontend
npm install
npm run dev
# 运行在 http://localhost:3006
```

## 环境变量

### 前端 (.env)
```
VITE_API_URL=http://localhost:8002  # 开发环境
VITE_API_URL=https://your-api.com   # 生产环境
```

### 后端
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
GITEE_CLIENT_ID=your_gitee_client_id
GITEE_CLIENT_SECRET=your_gitee_client_secret
```

## 技术栈

- **前端**: Vue 3 + Vite + Vue Router + Axios
- **后端**: FastAPI + PostgreSQL + JWT认证
- **部署**: Vercel (前端) + Railway (后端)
