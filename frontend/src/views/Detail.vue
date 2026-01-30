<template>
  <div class="detail-page">
    <!-- 头部导航 -->
    <header class="detail-header">
      <div class="container">
        <router-link to="/" class="back-link">
          <span class="back-icon">←</span>
          返回热搜榜
        </router-link>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="detail-content">
      <div class="container">
        <!-- 加载状态 -->
        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>正在加载详情内容...</p>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="error-container">
          <div class="error-icon">⚠️</div>
          <h2>加载失败</h2>
          <p>{{ error }}</p>
          <router-link to="/" class="back-btn">返回热搜榜</router-link>
        </div>

        <!-- 详情内容 -->
        <div v-else-if="detailData" class="detail-card">
          <!-- 排名和标题 -->
          <div class="detail-header-section">
            <div class="rank-badge" :class="getRankClass(detailData.rank)">
              {{ detailData.rank }}
            </div>
            <h1 class="detail-title">{{ detailData.title }}</h1>
            <p class="detail-meta">
              <span class="update-time">更新时间: {{ formatDate(detailData.created_at) }}</span>
            </p>
          </div>

          <!-- 图片区域 -->
          <div class="illustration-section">
            <img 
              v-if="detailData.image_url" 
              :src="detailData.image_url" 
              :alt="detailData.title" 
              class="detail-illustration"
              @error="handleImageError"
            />
            <img 
              v-else 
              :src="getIllustrationUrl(detailData.title)" 
              :alt="detailData.title" 
              class="detail-illustration"
            />
          </div>

          <!-- 内容区域 -->
          <div class="content-section">
            <h2>详细内容</h2>
            <div v-if="contentLoading" class="content-loading">
              <div class="loading-spinner small"></div>
              <p>正在抓取内容...</p>
            </div>
            <div v-else-if="contentError" class="content-error">
              <p>{{ contentError }}</p>
              <button @click="fetchContent" class="retry-btn">重试</button>
            </div>
            <div v-else-if="content" class="detail-content-text">
              {{ content }}
            </div>
            <div v-else class="content-placeholder">
              <p>点击下方链接查看完整内容</p>
            </div>
          </div>

          <!-- 原始链接 -->
          <div class="link-section">
            <h2>查看原始内容</h2>
            <a 
              :href="detailData.url" 
              target="_blank" 
              rel="noopener noreferrer" 
              class="original-link"
            >
              <span class="link-icon">🔗</span>
              {{ detailData.url }}
            </a>
          </div>
        </div>

        <!-- 未找到数据 -->
        <div v-else class="not-found">
          <div class="not-found-icon">🔍</div>
          <h2>未找到数据</h2>
          <p>该热搜内容不存在或已被删除</p>
          <router-link to="/" class="back-btn">返回热搜榜</router-link>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="detail-footer">
      <div class="container">
        <p>© {{ new Date().getFullYear() }} 百度热搜详情</p>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Detail',
  data() {
    return {
      detailData: null,
      content: null,
      isLoading: true,
      contentLoading: false,
      error: null,
      contentError: null
    }
  },
  mounted() {
    // 获取路由参数中的ID
    const id = this.$route.params.id
    if (id) {
      this.fetchDetailData(id)
    } else {
      this.error = '缺少必要参数'
      this.isLoading = false
    }
  },
  methods: {
    // 获取详情数据
    async fetchDetailData(id) {
      this.isLoading = true
      this.error = null
      
      try {
        // 这里应该调用后端API获取详情
        // 暂时使用模拟数据
        const response = await axios.get('/api/hot-search', {
          params: {
            page: 1,
            page_size: 100
          }
        })
        
        if (response.data && response.data.data) {
          const item = response.data.data.find(item => item.id == id)
          if (item) {
            this.detailData = item
            // 尝试抓取内容
            this.fetchContent()
          } else {
            this.error = '未找到该热搜内容'
          }
        } else {
          this.error = '获取数据失败'
        }
      } catch (err) {
        console.error('获取详情失败:', err)
        this.error = '网络错误，请稍后重试'
      } finally {
        this.isLoading = false
      }
    },
    
    // 尝试抓取内容
    async fetchContent() {
      if (!this.detailData) return
      
      this.contentLoading = true
      this.contentError = null
      
      try {
        // 由于跨域限制，这里使用模拟内容
        // 实际项目中可以通过后端代理抓取
        this.content = this.generateMockContent(this.detailData.title)
      } catch (err) {
        console.error('抓取内容失败:', err)
        this.contentError = '无法抓取内容，请直接访问原始链接'
      } finally {
        this.contentLoading = false
      }
    },
    
    // 生成模拟内容
    generateMockContent(title) {
      const contentTemplates = [
        `${title} 是当前网络上的热门话题，引起了广泛关注。该话题涉及多个方面，包括社会、经济、科技等领域。`,
        `关于 ${title} 的讨论在各大社交媒体平台上持续升温，网友们纷纷发表自己的看法和见解。`,
        `${title} 成为了人们茶余饭后的谈资，相关话题的搜索量持续攀升。`,
        `专家表示，${title} 反映了当前社会的一些重要趋势和问题，值得我们深入思考。`,
        `随着 ${title} 的热度不断上升，相关的新闻报道和分析文章也越来越多。`,
        `对于 ${title}，不同的人有不同的看法，这种多样性的观点也使得讨论更加丰富。`,
        `${title} 不仅仅是一个简单的热点话题，它背后可能蕴含着更深层次的社会意义。`,
        `在信息爆炸的时代，${title} 能够脱颖而出成为热搜，一定有其特殊的原因和价值。`
      ]
      
      let content = ''
      for (let i = 0; i < 3; i++) {
        const randomIndex = Math.floor(Math.random() * contentTemplates.length)
        content += contentTemplates[randomIndex] + '\n\n'
      }
      
      return content
    },
    
    // 获取排名对应的样式类
    getRankClass(rank) {
      if (rank === 1) return 'rank-1'
      if (rank === 2) return 'rank-2'
      if (rank === 3) return 'rank-3'
      return 'rank-other'
    },
    
    // 获取插画URL
    getIllustrationUrl(title) {
      // 使用Trae API生成相关插画
      const prompt = encodeURIComponent(`professional illustration for news article about ${title}, clean style, digital art, blue and white color scheme`)
      return `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=${prompt}&image_size=landscape_16_9`
    },
    
    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    // 处理图片加载错误
    handleImageError(event) {
      console.error('图片加载失败，使用随机图片')
      // 图片加载失败时，使用随机图片作为备用
      const randomImageId = Math.floor(Math.random() * 1000)
      event.target.src = `https://picsum.photos/seed/${randomImageId}/800/400`
    }
  }
}
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 头部导航 */
.detail-header {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 0;
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-link:hover {
  color: #0056b3;
  transform: translateX(-3px);
}

.back-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

/* 主内容区 */
.detail-content {
  flex: 1;
  padding: 2rem 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  gap: 1rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e9ecef;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-spinner.small {
  width: 24px;
  height: 24px;
  border-width: 2px;
}

.loading-container p {
  color: #6c757d;
  font-size: 1rem;
}

/* 错误状态 */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
  gap: 1.5rem;
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.error-icon {
  font-size: 3rem;
}

.error-container h2 {
  color: #dc3545;
  font-size: 1.5rem;
}

.error-container p {
  color: #6c757d;
  max-width: 400px;
}

.back-btn {
  padding: 0.75rem 1.5rem;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.back-btn:hover {
  background: #0056b3;
}

/* 详情卡片 */
.detail-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
}

/* 头部区域 */
.detail-header-section {
  padding: 2rem;
  border-bottom: 1px solid #f0f0f0;
  position: relative;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
  margin-bottom: 1rem;
}

.rank-1 {
  background: #dc3545;
}

.rank-2 {
  background: #fd7e14;
}

.rank-3 {
  background: #ffc107;
  color: #212529;
}

.rank-other {
  background: #6c757d;
}

.detail-title {
  font-size: 2rem;
  font-weight: 700;
  color: #343a40;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.detail-meta {
  display: flex;
  gap: 1.5rem;
  color: #6c757d;
  font-size: 0.875rem;
}

/* 插画区域 */
.illustration-section {
  padding: 0 2rem;
  margin: 1rem 0;
}

.detail-illustration {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.detail-illustration:hover {
  transform: scale(1.02);
}

/* 内容区域 */
.content-section {
  padding: 2rem;
  border-bottom: 1px solid #f0f0f0;
}

.content-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #343a40;
  margin-bottom: 1.5rem;
  position: relative;
  padding-bottom: 0.5rem;
}

.content-section h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: #007bff;
  border-radius: 2px;
}

.content-loading {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.content-error {
  padding: 2rem;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 8px;
  text-align: center;
  color: #721c24;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #721c24;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.retry-btn:hover {
  background: #5a181e;
}

.detail-content-text {
  line-height: 1.8;
  color: #495057;
  font-size: 1.05rem;
}

.content-placeholder {
  padding: 3rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
  color: #6c757d;
}

/* 链接区域 */
.link-section {
  padding: 2rem;
}

.link-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #343a40;
  margin-bottom: 1.5rem;
  position: relative;
  padding-bottom: 0.5rem;
}

.link-section h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: #007bff;
  border-radius: 2px;
}

.original-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  color: #007bff;
  text-decoration: none;
  transition: all 0.3s ease;
  word-break: break-all;
}

.original-link:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 2px 10px rgba(0, 123, 255, 0.1);
}

.link-icon {
  font-size: 1.2rem;
}

/* 未找到数据 */
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
  gap: 1.5rem;
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.not-found-icon {
  font-size: 4rem;
  color: #6c757d;
}

.not-found h2 {
  color: #495057;
  font-size: 1.5rem;
}

.not-found p {
  color: #6c757d;
  max-width: 400px;
}

/* 页脚 */
.detail-footer {
  background: rgba(255, 255, 255, 0.9);
  padding: 1.5rem 0;
  border-top: 1px solid #f0f0f0;
}

.detail-footer p {
  text-align: center;
  color: #6c757d;
  font-size: 0.875rem;
}

/* 动画 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .detail-title {
    font-size: 1.5rem;
  }

  .detail-illustration {
    height: 200px;
  }

  .detail-header-section,
  .content-section,
  .link-section {
    padding: 1.5rem;
  }

  .illustration-section {
    padding: 0 1.5rem;
  }
}

@media (max-width: 480px) {
  .detail-header-section {
    padding: 1.5rem;
  }

  .rank-badge {
    width: 32px;
    height: 32px;
    font-size: 1rem;
  }

  .detail-title {
    font-size: 1.3rem;
  }

  .detail-illustration {
    height: 160px;
  }

  .content-section h2,
  .link-section h2 {
    font-size: 1.2rem;
  }
}
</style>
