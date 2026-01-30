<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <div class="header-inner">
          <div class="logo">
            <span class="logo-icon">🔥</span>
            <h1 class="logo-text">百度热搜</h1>
          </div>
          <div class="header-meta">
            <span class="update-time">更新: {{ lastUpdateTime }}</span>
            <button class="refresh-btn" @click="fetchHotSearchData" :disabled="isRefreshing">
              <span class="refresh-icon" :class="{ spinning: isRefreshing }">↻</span>
              刷新
            </button>
          </div>
        </div>
      </div>
    </header>

    <nav class="category-nav">
      <div class="container">
        <div class="nav-list">
          <button 
            v-for="cat in categories" 
            :key="cat.value"
            :class="['nav-item', { active: currentCategory === cat.value }]"
            @click="switchCategory(cat.value)"
          >
            {{ cat.label }}
          </button>
        </div>
      </div>
    </nav>

    <main class="main">
      <div class="container">
        <div class="content-header">
          <h2 class="section-title">{{ currentCategoryLabel }}</h2>
          <span class="data-count">共 {{ total }} 条</span>
        </div>

        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>

        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button class="retry-btn" @click="fetchHotSearchData">重试</button>
        </div>

        <div v-else-if="filteredData.length === 0" class="empty-state">
          <p>暂无数据</p>
        </div>

        <div v-else class="data-list">
          <div 
            v-for="(item, index) in filteredData" 
            :key="item.id" 
            class="data-item"
            @click="navigateToDetail(item.id)"
          >
            <span class="item-rank" :class="getRankClass(item.rank)">{{ item.rank }}</span>
            <div class="item-content">
              <h3 class="item-title">{{ item.title }}</h3>
              <div class="item-meta">
                <span class="meta-time">{{ formatDate(item.created_at) }}</span>
                <span class="meta-hot">{{ item.hot_index }}</span>
              </div>
            </div>
            <span class="item-arrow">›</span>
          </div>
        </div>

        <div class="load-more" v-if="hasMore && !isLoading">
          <button class="load-more-btn" @click="loadMoreData" :disabled="isLoadingMore">
            {{ isLoadingMore ? '加载中...' : '加载更多' }}
          </button>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>© {{ new Date().getFullYear() }} 百度热搜榜</p>
    </footer>

    <button class="back-top" v-if="isScrolled" @click="scrollToTop">↑</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      hotSearchData: [],
      isLoading: false,
      isLoadingMore: false,
      isRefreshing: false,
      isScrolled: false,
      error: null,
      page: 1,
      pageSize: 20,
      hasMore: true,
      total: 0,
      currentCategory: 'realtime',
      lastUpdate: null,
      categories: [
        { value: 'realtime', label: '实时' },
        { value: 'movie', label: '影视' },
        { value: 'sport', label: '体育' },
        { value: 'tech', label: '科技' },
        { value: 'entertainment', label: '娱乐' }
      ]
    }
  },
  computed: {
    filteredData() {
      return this.hotSearchData
    },
    currentCategoryLabel() {
      const category = this.categories.find(cat => cat.value === this.currentCategory)
      return category ? category.label : '热搜'
    },
    lastUpdateTime() {
      if (this.lastUpdate) {
        return this.formatDate(this.lastUpdate)
      }
      return '--:--'
    }
  },
  mounted() {
    this.fetchHotSearchData()
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.isScrolled = document.documentElement.scrollTop > 200
    },
    switchCategory(category) {
      this.currentCategory = category
      this.fetchHotSearchData()
    },
    navigateToDetail(id) {
      this.$router.push({ name: 'Detail', params: { id } })
    },
    getRankClass(rank) {
      if (rank === 1) return 'rank-1'
      if (rank === 2) return 'rank-2'
      if (rank === 3) return 'rank-3'
      return ''
    },
    async fetchHotSearchData() {
      this.isLoading = true
      this.isRefreshing = true
      this.error = null
      this.page = 1
      this.hotSearchData = []
      this.hasMore = true

      try {
        const response = await axios.get('/api/hot-search', {
          params: {
            page: this.page,
            page_size: this.pageSize,
            category: this.currentCategory
          }
        })

        const data = response.data
        if (data.error) {
          this.error = data.error
          return
        }

        this.hotSearchData = data.data || []
        this.total = data.total || this.hotSearchData.length
        this.hasMore = this.hotSearchData.length >= this.pageSize
        this.lastUpdate = new Date()
      } catch (err) {
        console.error('获取数据失败:', err)
        this.error = '加载失败，请检查网络'
      } finally {
        this.isLoading = false
        this.isRefreshing = false
      }
    },
    async loadMoreData() {
      if (this.isLoadingMore || !this.hasMore) return
      this.isLoadingMore = true

      try {
        const nextPage = this.page + 1
        const response = await axios.get('/api/hot-search', {
          params: {
            page: nextPage,
            page_size: this.pageSize,
            category: this.currentCategory
          }
        })

        const data = response.data
        if (data.data && data.data.length > 0) {
          this.hotSearchData = [...this.hotSearchData, ...data.data]
          this.page = nextPage
          this.hasMore = data.data.length >= this.pageSize
        } else {
          this.hasMore = false
        }
      } catch (err) {
        console.error('加载更多失败:', err)
      } finally {
        this.isLoadingMore = false
      }
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date

      if (diff < 60000) return '刚刚'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
      
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

.app {
  min-height: 100vh;
  background: #fff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.container {
  max-width: 680px;
  margin: 0 auto;
  padding: 0 16px;
}

.header {
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
  padding: 14px 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.update-time {
  font-size: 12px;
  color: #999;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #333;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.refresh-btn:disabled {
  opacity: 0.6;
}

.refresh-icon {
  font-size: 14px;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.category-nav {
  background: #fff;
  border-bottom: 1px solid #eee;
}

.nav-list {
  display: flex;
  gap: 8px;
  padding: 10px 0;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.nav-list::-webkit-scrollbar {
  display: none;
}

.nav-item {
  padding: 8px 16px;
  background: #f5f5f5;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.nav-item:hover {
  background: #eee;
}

.nav-item.active {
  background: #333;
  color: #fff;
}

.main {
  padding: 16px 0;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.data-count {
  font-size: 13px;
  color: #999;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 2px solid #eee;
  border-top-color: #333;
  border-radius: 50%;
  margin: 0 auto 12px;
  animation: spin 1s linear infinite;
}

.retry-btn {
  margin-top: 12px;
  padding: 8px 20px;
  background: #333;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.data-list {
  border-top: 1px solid #eee;
}

.data-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 0;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
}

.item-rank {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  flex-shrink: 0;
}

.item-rank.rank-1 {
  background: #333;
  color: #fff;
}

.item-rank.rank-2 {
  background: #666;
  color: #fff;
}

.item-rank.rank-3 {
  background: #999;
  color: #fff;
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  line-height: 1.4;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #999;
}

.meta-hot {
  color: #ff6b6b;
}

.item-arrow {
  font-size: 18px;
  color: #ccc;
  flex-shrink: 0;
}

.load-more {
  text-align: center;
  padding: 20px;
}

.load-more-btn {
  padding: 10px 32px;
  background: #f5f5f5;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
}

.load-more-btn:disabled {
  opacity: 0.6;
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

.back-top {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 44px;
  height: 44px;
  background: #333;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  z-index: 100;
}

@media (max-width: 480px) {
  .header-inner {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .header-meta {
    width: 100%;
    justify-content: space-between;
  }

  .nav-item {
    padding: 6px 12px;
    font-size: 12px;
  }

  .data-item {
    padding: 12px 0;
  }

  .item-rank {
    width: 24px;
    height: 24px;
    font-size: 12px;
  }

  .item-title {
    font-size: 14px;
  }

  .back-top {
    bottom: 16px;
    right: 16px;
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
}
</style>
