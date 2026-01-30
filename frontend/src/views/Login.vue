<template>
    <div class="login-container">
        <div class="login-box">
            <div class="page-header">
                <h1>登录</h1>
                <p>欢迎回来，请登录您的账号</p>
            </div>
            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label for="username">用户名</label>
                    <input
                        type="text"
                        id="username"
                        v-model="username"
                        required
                        placeholder="请输入用户名"
                    />
                </div>
                <div class="form-group">
                    <label for="password">密码</label>
                    <input
                        type="password"
                        id="password"
                        v-model="password"
                        required
                        placeholder="请输入密码"
                    />
                </div>
                <div v-if="error" class="error-message">{{ error }}</div>
                <button type="submit" :disabled="loading">
                    {{ loading ? '登录中...' : '登录' }}
                </button>
            </form>
            
            <div class="divider">
                <span>其他登录方式</span>
            </div>
            
            <button class="gitee-btn" @click="handleGiteeLogin" :disabled="giteeLoading">
                <svg class="gitee-icon" viewBox="0 0 24 24" width="20" height="20">
                    <path fill="currentColor" d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                </svg>
                {{ giteeLoading ? '跳转中...' : 'Gitee 扫码登录' }}
            </button>
            
            <p class="register-link">
                还没有账号？<router-link to="/register">立即注册</router-link>
            </p>
        </div>
    </div>
</template>

<script>
import { login, setToken, giteeLogin, handleGiteeCallback } from '../api/auth'

export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
            error: '',
            loading: false,
            giteeLoading: false
        }
    },
    mounted() {
        this.checkGiteeCallback()
    },
    methods: {
        async handleLogin() {
            this.error = ''
            this.loading = true
            try {
                const data = await login(this.username, this.password)
                setToken(data.access_token)
                this.$router.push('/')
            } catch (err) {
                this.error = err.response?.data?.detail || '登录失败，请检查用户名和密码'
            } finally {
                this.loading = false
            }
        },
        async handleGiteeLogin() {
            this.giteeLoading = true
            try {
                await giteeLogin()
            } catch (err) {
                this.error = 'Gitee 登录失败，请稍后重试'
                this.giteeLoading = false
            }
        },
        checkGiteeCallback() {
            const token = this.$route.query.token
            const avatar = this.$route.query.avatar
            if (token) {
                handleGiteeCallback(token, avatar)
                this.$router.push('/')
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

.login-container {
    min-height: 100vh;
    background: #fff;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 60px 16px;
}

.login-box {
    max-width: 400px;
    margin: 0 auto;
}

.page-header {
    text-align: center;
    margin-bottom: 40px;
}

.page-header h1 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
}

.page-header p {
    font-size: 14px;
    color: #999;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    color: #666;
    font-size: 14px;
    font-weight: 500;
}

input {
    width: 100%;
    padding: 12px;
    border: 1px solid #eee;
    border-radius: 4px;
    font-size: 16px;
    color: #333;
    background: #fff;
    transition: border-color 0.3s;
}

input:focus {
    outline: none;
    border-color: #333;
}

input::placeholder {
    color: #999;
}

button {
    width: 100%;
    padding: 12px;
    background: #333;
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: opacity 0.3s;
}

button:hover:not(:disabled) {
    opacity: 0.9;
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.error-message {
    color: #dc3545;
    font-size: 14px;
    margin-bottom: 15px;
    padding: 10px;
    background: #f8d7da;
    border-radius: 4px;
}

.divider {
    display: flex;
    align-items: center;
    margin: 24px 0;
    color: #999;
    font-size: 14px;
}

.divider::before,
.divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #eee;
}

.divider span {
    padding: 0 15px;
}

.gitee-btn {
    width: 100%;
    padding: 12px;
    background: #fff;
    color: #333;
    border: 1px solid #eee;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.gitee-btn:hover:not(:disabled) {
    background: #f5f5f5;
    border-color: #ddd;
}

.gitee-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.gitee-icon {
    flex-shrink: 0;
}

.register-link {
    text-align: center;
    margin-top: 30px;
    font-size: 14px;
    color: #666;
}

.register-link a {
    color: #333;
    font-weight: 500;
    text-decoration: none;
}

.register-link a:hover {
    text-decoration: underline;
}

@media (max-width: 480px) {
    .login-container {
        padding: 40px 16px;
    }
}
</style>
