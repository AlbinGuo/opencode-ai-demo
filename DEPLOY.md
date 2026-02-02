# 部署指南

## 项目结构

```
vibe-coding/
├── api/                    # 后端 (FastAPI + PostgreSQL)
│   ├── main.py            # 主应用
│   ├── auth.py            # 认证模块
│   ├── jobs_spider.py     # 招聘爬虫
│   ├── baidu_hot_spider.py # 百度热搜爬虫
│   ├── railway.json       # Railway部署配置
│   └── .env.production    # 生产环境变量模板
├── frontend/              # 前端 (Vue 3 + Vite)
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   └── api/           # API封装
│   ├── vercel.json        # Vercel部署配置
│   └── .env.production    # 生产环境变量模板
└── DEPLOY.md             # 本部署文档
```

## 部署步骤

### 1. 部署后端到 Railway

1. **创建Railway项目**
   - 访问 [Railway](https://railway.app) 并登录
   - 点击 "New Project" → "Deploy from GitHub"
   - 选择本仓库

2. **配置数据库**
   - 在Railway项目页面，点击 "Add Database" → "PostgreSQL"
   - 等待数据库创建完成

3. **配置环境变量**
   - 点击 "Variables" 标签
   - 添加以下变量：
     ```
     ENVIRONMENT=production
     FRONTEND_URL=https://your-project.vercel.app
     GITEE_CLIENT_ID=your_gitee_client_id
     GITEE_CLIENT_SECRET=your_gitee_client_secret
     GITEE_REDIRECT_URI=https://your-backend.railway.app/auth/gitee/callback
     JWT_SECRET_KEY=your-super-secret-key-min-32-chars!!!
     ```
   - `DATABASE_URL` 会自动从PostgreSQL插件注入

4. **部署**
   - Railway会自动部署
   - 部署完成后获取后端URL，如：`https://your-app.railway.app`

5. **验证健康检查**
   ```
   https://your-app.railway.app/health
   ```

### 2. 部署前端到 Vercel

1. **创建Vercel项目**
   - 访问 [Vercel](https://vercel.com) 并登录
   - 点击 "Add New..." → "Project"
   - 导入本仓库

2. **配置构建**
   ```
   Build Command: npm run build
   Output Directory: dist
   Root Directory: frontend
   ```

3. **配置环境变量**
   - 点击 "Environment Variables"
   - 添加：
     ```
     VITE_API_URL=https://your-backend.railway.app
     ```

4. **部署**
   - 点击 "Deploy"
   - 部署完成后获取前端URL，如：`https://your-project.vercel.app`

### 3. 配置Gitee OAuth回调

1. 访问 [Gitee开发者设置](https://gitee.com/oauth/applications)
2. 编辑应用，回调地址改为：
   ```
   https://your-backend.railway.app/auth/gitee/callback
   ```

### 4. 测试完整流程

1. 打开前端：`https://your-project.vercel.app`
2. 测试热搜数据加载
3. 测试用户注册/登录
4. 测试Gitee第三方登录

## 部署验证

### 后端健康检查
```bash
curl https://your-backend.railway.app/health
# 预期返回: {"status":"healthy","database":"connected"}
```

### API测试
```bash
# 测试实时热搜
curl https://your-backend.railway.app/api/hot-search?category=realtime

# 测试影视热搜
curl https://your-backend.railway.app/api/hot-search?category=movie

# 测试体育热搜
curl https://your-backend.railway.app/api/hot-search?category=sport
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
# 运行在 http://localhost:3000
```

## 故障排查

### 1. CORS错误
- 检查后端 `ENVIRONMENT` 是否设置为 `production`
- 检查 `FRONTEND_URL` 是否正确设置为前端Vercel域名

### 2. 数据库连接失败
- 检查 `DATABASE_URL` 环境变量是否正确
- 确保PostgreSQL数据库已创建

### 3. Gitee登录失败
- 检查 `GITEE_CLIENT_ID` 和 `GITEE_CLIENT_SECRET` 是否正确
- 检查 `GITEE_REDIRECT_URI` 是否与Gitee设置中的一致
