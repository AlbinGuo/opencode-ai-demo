<template>
  <div class="app">
    <nav class="navbar">
      <div class="nav-content">
        <router-link to="/" class="nav-brand">百度热搜</router-link>
        <div class="nav-links">
          <template v-if="isLoggedIn">
            <router-link to="/jobs" class="nav-link">外企招聘</router-link>
            <div class="user-info">
              <img v-if="avatarUrl" :src="avatarUrl" alt="头像" class="user-avatar" />
              <div v-else class="user-avatar default-avatar">{{ username.charAt(0).toUpperCase() }}</div>
              <span class="welcome">{{ username }}</span>
            </div>
            <button @click="handleLogout" class="logout-btn">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-link">登录</router-link>
            <router-link to="/register" class="nav-link">注册</router-link>
          </template>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
import { isAuthenticated, logout, getToken, getCurrentUser } from './api/auth'

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      username: '',
      avatarUrl: ''
    }
  },
  mounted() {
    this.checkAuth()
  },
  watch: {
    '$route.path'() {
      this.checkAuth()
    }
  },
  methods: {
    async checkAuth() {
      this.isLoggedIn = isAuthenticated()
      if (this.isLoggedIn) {
        const user = localStorage.getItem('user')
        if (user) {
          try {
            const userData = JSON.parse(user)
            this.username = userData.gitee_id ? (userData.gitee_username || userData.username) : (userData.username || '用户')
            this.avatarUrl = userData.avatar_url || ''
          } catch (e) {
            this.username = '用户'
            this.avatarUrl = ''
          }
        } else {
          this.username = '用户'
          this.avatarUrl = ''
        }
        await this.fetchUserInfo()
      }
    },
    async fetchUserInfo() {
      try {
        const userData = await getCurrentUser()
        this.username = userData.gitee_id ? (userData.gitee_username || userData.username) : (userData.username || '用户')
        this.avatarUrl = userData.avatar_url || ''
        localStorage.setItem('user', JSON.stringify(userData))
      } catch (e) {
        console.error('获取用户信息失败:', e)
      }
    },
    handleLogout() {
      logout()
      this.isLoggedIn = false
      this.username = ''
      this.avatarUrl = ''
      this.$router.push('/login')
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

html {
  scroll-behavior: smooth;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #333;
  background-color: #fff;
  -webkit-font-smoothing: antialiased;
}

.app {
  min-height: 100vh;
}

.navbar {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: #666;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #007bff;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.default-avatar {
  background-color: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
}

.welcome {
  color: #666;
  font-size: 14px;
}

.logout-btn {
  padding: 8px 16px;
  background-color: transparent;
  color: #dc3545;
  border: 1px solid #dc3545;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover {
  background-color: #dc3545;
  color: white;
}

a {
  text-decoration: none;
  color: inherit;
}

button {
  font-family: inherit;
}

img {
  max-width: 100%;
  height: auto;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}
</style>
