<template>
  <div class="app">
    <!-- 分类菜单 -->
    <div class="category-menu">
      <div class="container">
        <div class="menu-container">
          <button 
            v-for="cat in categories" 
            :key="cat.value"
            :class="['category-btn', { active: currentCategory === cat.value }]"
            @click="switchCategory(cat.value)"
          >
            {{ cat.label }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 主内容区 -->
    <main class="main">
      <div class="container">
        <!-- 热搜数据表格 -->
        <div class="hot-search-table">
          <div class="table-header">
            <div class="table-cell rank">排名</div>
            <div class="table-cell image">图片</div>
            <div class="table-cell title">标题</div>
            <div class="table-cell action">操作</div>
          </div>
          
          <!-- 加载状态 -->
          <div v-if="isLoading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>正在加载热搜数据...</p>
          </div>
          
          <!-- 错误状态 -->
          <div v-else-if="error" class="error-state">
            <div class="error-icon">⚠️</div>
            <p>{{ error }}</p>
            <button @click="fetchHotSearchData" class="retry-btn">重试</button>
          </div>
          
          <!-- 数据列表 -->
          <div v-else class="table-body">
            <div 
              v-for="item in filteredData" 
              :key="item.id" 
              class="table-row"
              :class="{ 'top-rank': item.rank <= 3 }"
            >
              <div class="table-cell rank">
                <span class="rank-number" :class="{ 'top-1': item.rank === 1, 'top-2': item.rank === 2, 'top-3': item.rank === 3 }">
                  {{ item.rank }}
                </span>
              </div>
              <div class="table-cell image">
                <img 
                  v-if="item.image_url" 
                  :src="item.image_url" 
                  :alt="item.title" 
                  class="thumbnail"
                  @error="handleImageError"
                />
                <div v-else class="thumbnail-placeholder">
                  <span class="placeholder-icon">📰</span>
                </div>
              </div>
              <div class="table-cell title">
                <h3 class="title-text">{{ item.title }}</h3>
                <div class="title-meta">
                  <span class="created-at">{{ formatDate(item.created_at) }}</span>
                  <span v-if="item.hot_index" class="hot-index">{{ item.hot_index }} 热搜指数</span>
                </div>
              </div>
              <div class="table-cell action">
                <router-link 
                  :to="{ name: 'Detail', params: { id: item.id } }" 
                  class="action-btn view-btn"
                >
                  查看
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!isLoading && !error && filteredData.length === 0" class="empty-state">
            <div class="empty-icon">🔍</div>
            <p>没有找到匹配的热搜数据</p>
        </div>
        
        <!-- 加载更多指示器 -->
        <div v-if="isLoadingMore" class="loading-more">
            <div class="loading-spinner small"></div>
            <p>加载更多数据...</p>
        </div>
        
        <!-- 没有更多数据 -->
        <div v-if="!isLoadingMore && !hasMore && hotSearchData.length > 0" class="no-more">
            <p>没有更多数据了</p>
        </div>
        
        <!-- 用于Intersection Observer的触发元素 -->
        <div ref="loadTrigger" class="load-trigger"></div>
      </div>
    </main>
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
      error: null,
      page: 1,
      pageSize: 10,
      hasMore: true,
      total: 0,
      totalPages: 0,
      observer: null, // Intersection Observer实例
      refreshInterval: null, // 定时刷新定时器
      currentCategory: 'realtime', // 当前分类
      categories: [
        { value: 'realtime', label: '热搜' },
        { value: 'movie', label: '电影' },
        { value: 'sport', label: '体育' }
      ]
    }
  },
  computed: {
    // 直接返回原始数据
    filteredData() {
      return this.hotSearchData
    }
  },
  mounted() {
    // 组件挂载后获取数据
    this.fetchHotSearchData()
    
    // 等待DOM更新后初始化Intersection Observer
    this.$nextTick(() => {
      this.initIntersectionObserver()
    })
    
    // 设置定时刷新（每2分钟）
    this.refreshInterval = setInterval(() => {
      this.fetchHotSearchData()
      console.log('定时刷新热搜数据')
    }, 2 * 60 * 1000)
  },
  beforeUnmount() {
    // 清理Intersection Observer
    if (this.observer) {
      this.observer.disconnect()
    }
    
    // 清理定时刷新
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  },
  methods: {
    // 初始化Intersection Observer
    initIntersectionObserver() {
      if ('IntersectionObserver' in window && this.$refs.loadTrigger) {
        this.observer = new IntersectionObserver((entries) => {
          const entry = entries[0]
          if (entry.isIntersecting && !this.isLoadingMore && this.hasMore) {
            console.log('触发加载更多')
            this.loadMoreData()
          }
        }, {
          rootMargin: '0px 0px 200px 0px' // 提前200px触发
        })
        
        this.observer.observe(this.$refs.loadTrigger)
        console.log('Intersection Observer已初始化')
      } else {
        // 降级方案：使用滚动事件
        console.log('使用滚动事件作为降级方案')
        window.addEventListener('scroll', this.handleScroll)
      }
    },
    
    // 切换分类
    switchCategory(category) {
      this.currentCategory = category
      this.fetchHotSearchData()
    },
    
    // 获取热搜数据
    async fetchHotSearchData() {
      this.isLoading = true
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
        
        this.hotSearchData = data.data
        this.total = data.total
        this.totalPages = data.total_pages
        this.hasMore = this.page < this.totalPages
        console.log('初始数据加载完成，总数:', data.total, '页:', data.total_pages)
      } catch (err) {
        console.error('获取数据失败:', err)
        this.error = '获取热搜数据失败，请稍后重试'
      } finally {
        this.isLoading = false
      }
    },
    
    // 加载更多数据
    async loadMoreData() {
      if (this.isLoadingMore || !this.hasMore) return
      
      console.log('开始加载更多数据，当前页:', this.page)
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
        if (data.error) {
          console.error('加载更多数据失败:', data.error)
          return
        }
        
        console.log('加载更多数据成功，获取到:', data.data.length, '条')
        if (data.data.length > 0) {
          this.hotSearchData = [...this.hotSearchData, ...data.data]
          this.page = nextPage
          this.hasMore = this.page < data.total_pages
          console.log('更新后，当前页:', this.page, '是否有更多:', this.hasMore)
        } else {
          this.hasMore = false
          console.log('没有更多数据了')
        }
      } catch (err) {
        console.error('加载更多数据失败:', err)
      } finally {
        this.isLoadingMore = false
        console.log('加载更多数据完成')
      }
    },
    
    // 降级方案：处理滚动事件
    handleScroll() {
      const scrollTop = document.documentElement.scrollTop || document.body.scrollTop
      const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight
      const clientHeight = document.documentElement.clientHeight || window.innerHeight
      const distanceToBottom = scrollHeight - (scrollTop + clientHeight)
      
      // 当滚动到距离底部50px时加载更多
      if (distanceToBottom <= 50 && !this.isLoadingMore && this.hasMore) {
        console.log('触发加载更多，距离底部:', distanceToBottom, 'px')
        this.loadMoreData()
      }
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
      // 图片加载失败时，使用随机图片
      console.log('图片加载失败，使用随机图片')
      // 使用随机图片作为备用
      const randomImageId = Math.floor(Math.random() * 1000)
      event.target.src = `https://picsum.photos/seed/${randomImageId}/200/200`
      event.target.style.display = 'block'
      // 隐藏占位符
      if (event.target.nextElementSibling) {
        event.target.nextElementSibling.style.display = 'none'
      }
    }
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
}

/* 分类菜单 */
.category-menu {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-bottom: 1px solid #e9ecef;
  padding: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.menu-container {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.category-btn {
  padding: 0.625rem 1.25rem;
  border: 1px solid #dee2e6;
  background: #ffffff;
  border-radius: 25px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.category-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.category-btn:hover::before {
  left: 100%;
}

.category-btn:hover {
  background: #f8f9fa;
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.1);
}

.category-btn.active {
  background: linear-gradient(135deg, #007bff 0%, #0069d9 100%);
  color: white;
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

.category-btn.active:hover {
  background: linear-gradient(135deg, #0069d9 0%, #0056b3 100%);
  border-color: #0062cc;
}

/* 添加分类图标 */
.category-btn::after {
  content: '';
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-left: 8px;
  vertical-align: middle;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.category-btn:nth-child(1)::after {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>');
}

.category-btn:nth-child(2)::after {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4h-4zm-6 14c-2.33 0-7-1.17-7-3v-2c0-.55.45-1 1-1h12c.55 0 1 .45 1 1v2c0 1.83-4.67 3-7 3z"/></svg>');
}

.category-btn:nth-child(3)::after {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M18.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm-2.5 0v2.21c1.48-.73 2.5-2.25 2.5-4.03 0-.22-.02-.43-.05-.63l-2.45 2.45zM14 16.5v-9l6 4.5-6 4.5zM3 10.5h8v3H3v-3zm5-6H3v3h5V4.5zm-5 9h8v3H3v-3zm5-6v3H3v-3h5z"/></svg>');
}

/* 主内容区 */
.main {
  flex: 1;
  padding: 1rem 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1rem;
}

.hot-search-table {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  margin-bottom: 1rem;
}

.table-header {
  display: grid;
  grid-template-columns: 60px 80px 1fr 80px;
  background: #f8f9fa;
  color: #495057;
  padding: 0.75rem;
  font-weight: 600;
  font-size: 0.875rem;
  border-bottom: 1px solid #e9ecef;
}

.table-row {
  display: grid;
  grid-template-columns: 60px 80px 1fr 80px;
  padding: 0.75rem;
  border-bottom: 1px solid #e9ecef;
  transition: background-color 0.2s ease;
}

/* 隐藏表格头部的标题列 */
.table-header {
  display: none;
}

/* 图片列样式 */
.table-cell.image {
  display: flex;
  align-items: center;
  justify-content: center;
}

.thumbnail {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.thumbnail:hover {
  transform: scale(1.05);
}

.thumbnail-placeholder {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
}

.placeholder-icon {
  font-size: 1.5rem;
  opacity: 0.5;
}

/* 标题元数据样式 */
.title-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-top: 0.25rem;
}

.hot-index {
  font-size: 0.75rem;
  color: #dc3545;
  font-weight: 500;
  background: #f8d7da;
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  white-space: nowrap;
}

.table-row:hover {
  background: #f8f9fa;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row.top-rank {
  background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
}

/* 为前三名分别设置不同的渐变背景色 */
.table-row:nth-child(1) {
  background: linear-gradient(135deg, #ffe6e6 0%, #ffcccc 100%);
}

.table-row:nth-child(2) {
  background: linear-gradient(135deg, #fff0e6 0%, #ffd9cc 100%);
}

.table-row:nth-child(3) {
  background: linear-gradient(135deg, #fff9e6 0%, #ffebcc 100%);
}

.table-cell {
  display: flex;
  align-items: center;
}

.table-cell.rank {
  justify-content: center;
}

.table-cell.title {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.25rem;
}

.table-cell.action {
  justify-content: center;
}

.rank-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.75rem;
  color: #495057;
  background: #e9ecef;
}

.rank-number.top-1 {
  background: #dc3545;
  color: white;
}

.rank-number.top-2 {
  background: #fd7e14;
  color: white;
}

.rank-number.top-3 {
  background: #ffc107;
  color: #212529;
}

.title-text {
  font-size: 0.875rem;
  font-weight: 400;
  color: #495057;
  line-height: 1.4;
}

/* 隐藏列表顶部的title */
.table-header .table-cell.title {
  display: none;
}

.created-at {
  font-size: 0.75rem;
  color: #6c757d;
}

.action-btn {
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.view-btn {
  background: #007bff;
  color: white;
  border: 1px solid #007bff;
}

.view-btn:hover {
  background: #0069d9;
  border-color: #0062cc;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 0.75rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #e9ecef;
  border-top: 2px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-state p {
  font-size: 0.875rem;
  color: #6c757d;
  margin: 0;
}

/* 错误状态 */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
  text-align: center;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

.error-icon {
  font-size: 1.5rem;
}

.error-state p {
  font-size: 0.875rem;
  color: #dc3545;
  max-width: 350px;
  margin: 0;
}

.retry-btn {
  padding: 0.4rem 0.8rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.retry-btn:hover {
  background: #0069d9;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 0.75rem;
  text-align: center;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  color: #6c757d;
}

.empty-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.empty-state p {
  font-size: 0.875rem;
  margin: 0;
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

/* 加载更多样式 */
.loading-more {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  gap: 0.5rem;
  background: #ffffff;
  border-radius: 8px;
  margin-top: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

.loading-spinner.small {
  width: 20px;
  height: 20px;
  border-width: 2px;
}

.loading-more p {
  font-size: 0.875rem;
  color: #6c757d;
  margin: 0;
}

.no-more {
  text-align: center;
  padding: 1rem;
  background: #ffffff;
  border-radius: 8px;
  margin-top: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  color: #6c757d;
}

.no-more p {
  font-size: 0.875rem;
  margin: 0;
}

/* 加载触发元素 */
.load-trigger {
  height: 20px;
  width: 100%;
  margin-top: 1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 0 0.75rem;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 50px 1fr 70px;
    padding: 0.6rem;
  }
  
  .rank-number {
    width: 20px;
    height: 20px;
    font-size: 0.75rem;
  }
  
  .title-text {
    font-size: 0.8125rem;
  }
  
  .created-at {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .table-header,
  .table-row {
    grid-template-columns: 40px 1fr;
    gap: 0.5rem;
  }
  
  .table-header .action,
  .table-row .action {
    display: none;
  }
}
</style>
