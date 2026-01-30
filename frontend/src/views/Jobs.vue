<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <div class="header-inner">
          <div class="logo">
            <span class="logo-icon">💼</span>
            <h1 class="logo-text">外企招聘</h1>
          </div>
          <div class="header-meta">
            <span class="update-time">共 {{ total }} 条职位</span>
          </div>
        </div>
      </div>
    </header>

    <nav class="filter-nav">
      <div class="container">
        <div class="filter-row">
          <div class="filter-item">
            <label>城市</label>
            <select v-model="selectedCity" @change="fetchJobs">
              <option value="">选择城市</option>
              <option v-for="city in cities" :key="city.code" :value="city.code">
                {{ city.name }}
              </option>
            </select>
          </div>
          <div class="filter-item">
            <label>职位</label>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Python/Java/产品..."
              @keyup.enter="fetchJobs"
            />
          </div>
          <button class="search-btn" @click="fetchJobs" :disabled="isLoading">
            {{ isLoading ? '搜索中...' : '搜索' }}
          </button>
        </div>
      </div>
    </nav>

    <main class="main">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">🔥 热门外企职位</h2>
        </div>

        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>正在加载职位信息...</p>
        </div>

        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button class="retry-btn" @click="fetchJobs">重试</button>
        </div>

        <div v-else-if="jobs.length === 0" class="empty-state">
          <p>暂无符合条件的职位</p>
        </div>

        <div v-else class="job-list">
          <div 
            v-for="(job, index) in jobs" 
            :key="job.id" 
            class="job-item"
            @click="openJobDetail(job.id)"
          >
            <div class="job-left">
              <div class="job-salary">{{ job.salary_range }}</div>
              <h3 class="job-title">{{ job.job_name }}</h3>
              <div class="job-tags">
                <span class="tag">{{ job.city }}</span>
                <span class="tag">{{ job.experience }}</span>
                <span class="tag">{{ job.education }}</span>
              </div>
            </div>
            <div class="job-right">
              <div class="company-name">{{ job.company_name }}</div>
              <div class="company-info">
                <span class="scale">{{ job.company_scale }}</span>
                <span class="dot">·</span>
                <span class="industry">{{ job.company_industry }}</span>
                <span class="dot">·</span>
                <span class="finance">{{ job.finance_stage }}</span>
              </div>
              <div class="job-benefits">
                <span v-for="(benefit, i) in job.job_benefits.slice(0, 3)" :key="i" class="benefit">
                  {{ benefit }}
                </span>
              </div>
            </div>
            <img 
              v-if="job.company_logo" 
              :src="job.company_logo" 
              class="company-logo" 
              @error="handleLogoError"
            />
            <div v-else class="company-logo-placeholder">
              {{ getCompanyInitial(job.company_name) }}
            </div>
            <span class="job-arrow">›</span>
          </div>
        </div>

        <div class="load-more" v-if="hasMore && !isLoading">
          <button class="load-more-btn" @click="loadMore" :disabled="isLoadingMore">
            {{ isLoadingMore ? '加载中...' : '加载更多' }}
          </button>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>© {{ new Date().getFullYear() }} 外企招聘 - 数据来源：BOSS直聘</p>
    </footer>

    <button class="back-top" v-if="isScrolled" @click="scrollToTop">↑</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Jobs',
  data() {
    return {
      jobs: [],
      isLoading: false,
      isLoadingMore: false,
      isScrolled: false,
      error: null,
      page: 1,
      pageSize: 10,
      hasMore: true,
      total: 0,
      searchQuery: '',
      selectedCity: '',
      cities: [
        { code: '101200300', name: '西安' },
        { code: '101010100', name: '北京' },
        { code: '101020100', name: '上海' },
        { code: '101280100', name: '广州' },
        { code: '101280600', name: '深圳' },
        { code: '101210100', name: '杭州' },
        { code: '101230200', name: '成都' },
        { code: '101200100', name: '武汉' },
        { code: '101190400', name: '南京' }
      ]
    }
  },
  mounted() {
    this.fetchJobs()
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.isScrolled = document.documentElement.scrollTop > 200
    },
    async fetchJobs() {
      this.isLoading = true
      this.error = null
      this.page = 1
      this.jobs = []
      this.hasMore = true

      try {
        const response = await axios.get('/api/jobs', {
          params: {
            query: this.searchQuery,
            city: this.selectedCity,
            page: this.page,
            page_size: this.pageSize
          }
        })
        const data = response.data
        
        if (data.error) {
          this.error = data.error
          return
        }

        this.jobs = data.data || []
        this.total = data.total || this.jobs.length
        this.hasMore = this.jobs.length >= this.pageSize
      } catch (err) {
        console.error('获取职位失败:', err)
        this.error = '加载失败，请检查网络'
      } finally {
        this.isLoading = false
      }
    },
    async loadMore() {
      if (this.isLoadingMore || !this.hasMore) return
      this.isLoadingMore = true

      try {
        this.page++
        const response = await axios.get('/api/jobs', {
          params: {
            query: this.searchQuery,
            city: this.selectedCity,
            page: this.page,
            page_size: this.pageSize
          }
        })
        const data = response.data
        
        if (data.data && data.data.length > 0) {
          this.jobs = [...this.jobs, ...data.data]
          this.hasMore = data.data.length >= this.pageSize
        } else {
          this.hasMore = false
        }
      } catch (err) {
        console.error('加载更多失败:', err)
        this.page--
      } finally {
        this.isLoadingMore = false
      }
    },
    openJobDetail(jobId) {
      this.$router.push(`/jobs/${jobId}`)
    },
    getCompanyInitial(name) {
      if (!name) return '?'
      return name.charAt(0).toUpperCase()
    },
    handleLogoError(e) {
      e.target.style.display = 'none'
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
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

.filter-nav {
  background: #fff;
  border-bottom: 1px solid #eee;
  padding: 12px 0;
}

.filter-row {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.filter-item {
  flex: 1;
}

.filter-item label {
  display: block;
  font-size: 12px;
  color: #666;
  margin-bottom: 6px;
}

.filter-item select,
.filter-item input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #eee;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  background: #fff;
}

.filter-item select:focus,
.filter-item input:focus {
  outline: none;
  border-color: #333;
}

.search-btn {
  padding: 10px 20px;
  background: #333;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
}

.search-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.main {
  padding: 16px 0;
}

.section-header {
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

@keyframes spin {
  to { transform: rotate(360deg); }
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

.job-list {
  border-top: 1px solid #eee;
}

.job-item {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  position: relative;
}

.job-left {
  flex-shrink: 0;
  width: 100px;
}

.job-salary {
  font-size: 16px;
  font-weight: 600;
  color: #ff6b6b;
  margin-bottom: 8px;
}

.job-title {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  line-height: 1.4;
  margin-bottom: 8px;
}

.job-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  font-size: 12px;
  color: #666;
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 2px;
}

.job-right {
  flex: 1;
  min-width: 0;
}

.company-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.company-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.dot {
  color: #ddd;
}

.job-benefits {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.benefit {
  font-size: 12px;
  color: #07c160;
  background: #e8f5e9;
  padding: 2px 8px;
  border-radius: 2px;
}

.job-arrow {
  font-size: 18px;
  color: #ccc;
  flex-shrink: 0;
  margin-left: 8px;
}

.company-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 8px;
  border: 1px solid #eee;
  flex-shrink: 0;
}

.company-logo-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 18px;
  font-weight: 600;
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
  .filter-row {
    flex-wrap: wrap;
  }
  
  .filter-item {
    flex: 1 1 45%;
  }
  
  .search-btn {
    flex: 0 0 auto;
  }
  
  .job-left {
    width: 80px;
  }
  
  .job-salary {
    font-size: 14px;
  }
  
  .job-title {
    font-size: 14px;
  }
}
</style>
