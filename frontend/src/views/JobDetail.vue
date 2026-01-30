<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <div class="header-inner">
          <router-link to="/jobs" class="back-link">
            <span class="back-icon">‹</span>
            返回职位列表
          </router-link>
          <div class="header-title">职位详情</div>
        </div>
      </div>
    </header>

    <main class="main">
      <div class="container" v-if="job">
        <div class="job-card">
          <div class="job-header">
            <div class="job-salary">{{ job.salary_range }}</div>
            <h1 class="job-name">{{ job.job_name }}</h1>
            <div class="job-company">
              <span class="company-name">{{ job.company_name }}</span>
              <span class="dot">·</span>
              <span class="company-info">{{ job.city }} {{ job.district }}</span>
            </div>
          </div>

          <div class="job-tags-row">
            <span class="tag">{{ job.experience }}</span>
            <span class="tag">{{ job.education }}</span>
            <span class="tag">{{ job.finance_stage }}</span>
            <span class="tag">{{ job.company_scale }}</span>
          </div>

          <div class="job-section">
            <h3 class="section-title">公司信息</h3>
            <div class="company-detail">
              <div class="detail-row">
                <span class="label">公司名称</span>
                <span class="value">{{ job.company_name }}</span>
              </div>
              <div class="detail-row">
                <span class="label">公司规模</span>
                <span class="value">{{ job.company_scale }}</span>
              </div>
              <div class="detail-row">
                <span class="label">所属行业</span>
                <span class="value">{{ job.company_industry }}</span>
              </div>
              <div class="detail-row">
                <span class="label">融资阶段</span>
                <span class="value">{{ job.finance_stage }}</span>
              </div>
            </div>
          </div>

          <div class="job-section">
            <h3 class="section-title">职位信息</h3>
            <div class="job-detail">
              <div class="detail-row">
                <span class="label">职位名称</span>
                <span class="value">{{ job.job_name }}</span>
              </div>
              <div class="detail-row">
                <span class="label">工作地点</span>
                <span class="value">{{ job.city }} {{ job.district }}</span>
              </div>
              <div class="detail-row">
                <span class="label">经验要求</span>
                <span class="value">{{ job.experience }}</span>
              </div>
              <div class="detail-row">
                <span class="label">学历要求</span>
                <span class="value">{{ job.education }}</span>
              </div>
              <div class="detail-row">
                <span class="label">薪资范围</span>
                <span class="value salary">{{ job.salary_range }}</span>
              </div>
              <div class="detail-row">
                <span class="label">发布时间</span>
                <span class="value">{{ job.posted_time }}</span>
              </div>
            </div>
          </div>

          <div class="job-section" v-if="job.job_benefits && job.job_benefits.length > 0">
            <h3 class="section-title">公司福利</h3>
            <div class="benefits-list">
              <span v-for="(benefit, index) in job.job_benefits" :key="index" class="benefit-tag">
                {{ benefit }}
              </span>
            </div>
          </div>

          <div class="job-actions">
            <a :href="job.detail_url" target="_blank" class="apply-btn">
              投递简历
            </a>
            <a :href="job.detail_url" target="_blank" class="detail-btn">
              查看原详情
            </a>
          </div>
        </div>
      </div>

      <div v-else-if="isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else class="error-state">
        <p>{{ error || '职位不存在' }}</p>
        <router-link to="/jobs" class="back-btn">返回职位列表</router-link>
      </div>
    </main>

    <footer class="footer">
      <p>© {{ new Date().getFullYear() }} 外企招聘 - 数据来源：BOSS直聘</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'JobDetail',
  data() {
    return {
      job: null,
      isLoading: false,
      error: null
    }
  },
  mounted() {
    this.fetchJobDetail()
  },
  methods: {
    async fetchJobDetail() {
      const jobId = this.$route.params.id
      if (!jobId) {
        this.error = '职位ID不存在'
        return
      }

      this.isLoading = true
      this.error = null

      try {
        const response = await axios.get(`/api/jobs/${jobId}`)
        if (response.data && response.data.data) {
          const jobData = response.data.data
          if (typeof jobData.job_benefits === 'string') {
            try {
              jobData.job_benefits = JSON.parse(jobData.job_benefits)
            } catch (e) {
              jobData.job_benefits = []
            }
          }
          this.job = jobData
        } else {
          this.error = '职位不存在'
        }
      } catch (err) {
        console.error('获取职位详情失败:', err)
        this.error = '加载失败，请稍后重试'
      } finally {
        this.isLoading = false
      }
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
  background: #f5f5f5;
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
  align-items: center;
  padding: 14px 0;
  gap: 16px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #666;
  font-size: 14px;
  text-decoration: none;
  flex-shrink: 0;
}

.back-link:hover {
  color: #333;
}

.back-icon {
  font-size: 20px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.main {
  padding: 20px 0;
}

.job-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.job-header {
  padding: 24px 20px 20px;
  border-bottom: 1px solid #f5f5f5;
}

.job-salary {
  font-size: 24px;
  font-weight: 600;
  color: #ff6b6b;
  margin-bottom: 12px;
}

.job-name {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.4;
}

.job-company {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.dot {
  color: #ddd;
}

.job-tags-row {
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  flex-wrap: wrap;
  background: #fafafa;
}

.tag {
  font-size: 12px;
  color: #666;
  background: #f5f5f5;
  padding: 4px 10px;
  border-radius: 4px;
}

.job-section {
  padding: 20px;
  border-bottom: 1px solid #f5f5f5;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f5f5f5;
}

.detail-row:last-child {
  border-bottom: none;
}

.label {
  font-size: 14px;
  color: #999;
}

.value {
  font-size: 14px;
  color: #333;
}

.value.salary {
  font-weight: 600;
  color: #ff6b6b;
}

.benefits-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.benefit-tag {
  font-size: 12px;
  color: #07c160;
  background: #e8f5e9;
  padding: 4px 12px;
  border-radius: 4px;
}

.job-actions {
  padding: 24px 20px;
  display: flex;
  gap: 12px;
}

.apply-btn {
  flex: 1;
  padding: 14px;
  background: #ff6b6b;
  color: #fff;
  text-align: center;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  transition: opacity 0.3s;
}

.apply-btn:hover {
  opacity: 0.9;
}

.detail-btn {
  flex: 1;
  padding: 14px;
  background: #fff;
  color: #333;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  text-decoration: none;
  transition: all 0.3s;
}

.detail-btn:hover {
  background: #f5f5f5;
}

.loading-state,
.error-state {
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

.back-btn {
  display: inline-block;
  margin-top: 16px;
  padding: 10px 24px;
  background: #333;
  color: #fff;
  border-radius: 4px;
  text-decoration: none;
}

.footer {
  text-align: center;
  padding: 24px;
  margin-top: 20px;
}

.footer p {
  font-size: 12px;
  color: #999;
}

@media (max-width: 480px) {
  .job-actions {
    flex-direction: column;
  }
}
</style>
