<template>
  <div class="detail-page">
    <header class="detail-header">
      <div class="container">
        <div class="header-inner">
          <router-link to="/" class="back-link">
            <span>‹</span> 返回
          </router-link>
          <button class="share-btn" @click="shareContent">分享</button>
        </div>
      </div>
    </header>

    <main class="detail-content">
      <div class="container">
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>

        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <router-link to="/" class="back-btn">返回首页</router-link>
        </div>

        <template v-else-if="detailData">
          <article class="article">
            <header class="article-header">
              <div class="article-rank">
                <span class="rank-num">{{ detailData.rank }}</span>
                <span class="rank-label">热度</span>
              </div>
              <h1 class="article-title">{{ detailData.title }}</h1>
              <div class="article-meta">
                <span>{{ formatDate(detailData.created_at) }}</span>
                <span class="meta-hot">{{ detailData.hot_index }}</span>
              </div>
            </header>

            <div class="article-image" v-if="detailData.image_url">
              <img :src="detailData.image_url" :alt="detailData.title" @error="handleImageError" />
            </div>

            <section class="article-body">
              <h2 class="section-title">内容详情</h2>
              <div v-if="contentLoading" class="content-loading">
                <span class="loading-dots">...</span>
              </div>
              <div v-else-if="content" class="content-text">
                <p v-for="(para, idx) in content.split('\n\n')" :key="idx">{{ para }}</p>
              </div>
              <p v-else class="content-placeholder">暂无详细内容</p>
            </section>

            <section class="article-link">
              <h2 class="section-title">原文链接</h2>
              <a :href="detailData.url" target="_blank" rel="noopener" class="link-box">
                <span class="link-text">{{ detailData.url }}</span>
                <span class="link-icon">↗</span>
              </a>
            </section>
          </article>

          <aside class="related">
            <h2 class="related-title">相关推荐</h2>
            <div class="related-list">
              <div 
                v-for="(item, idx) in relatedItems" 
                :key="idx"
                class="related-item"
                @click="navigateToDetail(item.id)"
              >
                <span class="related-rank">{{ item.rank }}</span>
                <span class="related-title">{{ item.title }}</span>
              </div>
              <p v-if="relatedItems.length === 0" class="related-empty">暂无相关内容</p>
            </div>
          </aside>
        </template>

        <div v-else class="not-found">
          <p>内容不存在</p>
          <router-link to="/" class="back-btn">返回首页</router-link>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>© {{ new Date().getFullYear() }} 百度热搜</p>
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
      relatedItems: []
    }
  },
  mounted() {
    const id = this.$route.params.id
    if (id) {
      this.fetchDetailData(id)
    } else {
      this.error = '参数错误'
      this.isLoading = false
    }
  },
  methods: {
    async fetchDetailData(id) {
      this.isLoading = true
      this.error = null

      try {
        const response = await axios.get('/api/hot-search', {
          params: { page: 1, page_size: 100 }
        })

        if (response.data && response.data.data) {
          const item = response.data.data.find(x => x.id == id)
          if (item) {
            this.detailData = item
            this.fetchContent()
            this.fetchRelatedItems(id)
          } else {
            this.error = '内容不存在'
          }
        } else {
          this.error = '加载失败'
        }
      } catch (err) {
        console.error('获取详情失败:', err)
        this.error = '网络错误'
      } finally {
        this.isLoading = false
      }
    },
    fetchContent() {
      if (!this.detailData) return
      this.contentLoading = true
      setTimeout(() => {
        const titles = [
          '该话题引发广泛关注，社交媒体讨论热度持续攀升。',
          '各界人士对此发表看法，观点多元且深入。',
          '相关话题阅读量突破亿次，成为当日焦点。',
          '专家分析认为，这一现象反映了当前社会的重要趋势。'
        ]
        this.content = titles.slice(0, 3).join('\n\n')
        this.contentLoading = false
      }, 500)
    },
    fetchRelatedItems(currentId) {
      axios.get('/api/hot-search', { params: { page: 1, page_size: 10 } })
        .then(res => {
          if (res.data && res.data.data) {
            this.relatedItems = res.data.data
              .filter(x => x.id != currentId)
              .slice(0, 5)
          }
        })
        .catch(() => {})
    },
    navigateToDetail(id) {
      this.$router.push({ name: 'Detail', params: { id } })
    },
    shareContent() {
      if (!this.detailData) return
      const text = `${this.detailData.title} - 排名第${this.detailData.rank}`
      if (navigator.share) {
        navigator.share({ title: '百度热搜', text, url: window.location.href })
      } else {
        navigator.clipboard.writeText(`${text}\n${window.location.href}`)
        alert('链接已复制')
      }
    },
    handleImageError(e) {
      e.target.style.display = 'none'
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.detail-page {
  min-height: 100vh;
  background: #fff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.container {
  max-width: 680px;
  margin: 0 auto;
  padding: 0 16px;
}

.detail-header {
  background: #fff;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #333;
}

.back-link span {
  font-size: 18px;
}

.share-btn {
  padding: 6px 14px;
  background: #333;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.detail-content {
  padding: 20px 0;
}

.loading-state,
.error-state,
.not-found {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.loading-spinner {
  width: 28px;
  height: 28px;
  border: 2px solid #eee;
  border-top-color: #333;
  border-radius: 50%;
  margin: 0 auto 12px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.back-btn {
  display: inline-block;
  margin-top: 12px;
  padding: 8px 20px;
  background: #333;
  color: #fff;
  border-radius: 4px;
  font-size: 14px;
}

.article {
  margin-bottom: 24px;
}

.article-header {
  margin-bottom: 16px;
}

.article-rank {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: #333;
  color: #fff;
  border-radius: 6px;
  margin-bottom: 12px;
}

.rank-num {
  font-size: 18px;
  font-weight: 600;
}

.rank-label {
  font-size: 10px;
  opacity: 0.8;
}

.article-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  line-height: 1.5;
  margin-bottom: 10px;
}

.article-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #999;
}

.meta-hot {
  color: #ff6b6b;
}

.article-image {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.article-image img {
  width: 100%;
  display: block;
}

.article-body,
.article-link {
  margin-bottom: 20px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  padding-left: 8px;
  border-left: 3px solid #333;
}

.content-loading {
  padding: 20px;
  color: #999;
}

.loading-dots {
  font-size: 20px;
  letter-spacing: 4px;
}

.content-text p {
  font-size: 15px;
  line-height: 1.8;
  color: #444;
  margin-bottom: 12px;
}

.content-placeholder {
  color: #999;
  font-size: 14px;
}

.link-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 6px;
  text-decoration: none;
}

.link-text {
  flex: 1;
  font-size: 13px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 8px;
}

.link-icon {
  font-size: 16px;
  color: #999;
}

.related {
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.related-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.related-list {
  display: flex;
  flex-direction: column;
}

.related-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
}

.related-item:last-child {
  border-bottom: none;
}

.related-rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
  flex-shrink: 0;
}

.related-title {
  flex: 1;
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-empty {
  color: #999;
  font-size: 14px;
  padding: 20px 0;
}

.footer {
  text-align: center;
  padding: 24px;
  border-top: 1px solid #eee;
  margin-top: 20px;
}

.footer p {
  font-size: 12px;
  color: #999;
}

@media (max-width: 480px) {
  .article-title {
    font-size: 18px;
  }

  .article-meta {
    flex-direction: column;
    gap: 4px;
  }

  .content-text p {
    font-size: 14px;
  }

  .related-item {
    padding: 10px 0;
  }

  .related-title {
    font-size: 13px;
  }
}
</style>
