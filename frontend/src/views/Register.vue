<template>
    <div class="register-container">
        <div class="register-box">
            <div class="page-header">
                <h1>注册</h1>
                <p>创建您的账号，开启热搜之旅</p>
            </div>
            <form @submit.prevent="handleRegister">
                <div class="form-group">
                    <label for="username">用户名</label>
                    <input
                        type="text"
                        id="username"
                        v-model="username"
                        required
                        placeholder="请输入用户名（3-20个字符）"
                        minlength="3"
                        maxlength="20"
                    />
                </div>
                <div class="form-group">
                    <label for="email">邮箱</label>
                    <input
                        type="email"
                        id="email"
                        v-model="email"
                        required
                        placeholder="请输入邮箱"
                    />
                </div>
                <div class="form-group">
                    <label for="password">密码</label>
                    <input
                        type="password"
                        id="password"
                        v-model="password"
                        required
                        placeholder="请输入密码（至少6个字符）"
                        minlength="6"
                    />
                </div>
                <div class="form-group">
                    <label for="confirmPassword">确认密码</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        v-model="confirmPassword"
                        required
                        placeholder="请再次输入密码"
                    />
                </div>
                <div v-if="error" class="error-message">{{ error }}</div>
                <div v-if="success" class="success-message">{{ success }}</div>
                <button type="submit" :disabled="loading">
                    {{ loading ? '注册中...' : '注册' }}
                </button>
            </form>
            <p class="login-link">
                已有账号？<router-link to="/login">立即登录</router-link>
            </p>
        </div>
    </div>
</template>

<script>
import { register } from '../api/auth'

export default {
    name: 'Register',
    data() {
        return {
            username: '',
            email: '',
            password: '',
            confirmPassword: '',
            error: '',
            success: '',
            loading: false
        }
    },
    methods: {
        async handleRegister() {
            this.error = ''
            this.success = ''
            
            if (this.password !== this.confirmPassword) {
                this.error = '两次输入的密码不一致'
                return
            }
            
            this.loading = true
            try {
                await register(this.username, this.email, this.password)
                this.success = '注册成功！正在跳转到登录页面...'
                setTimeout(() => {
                    this.$router.push('/login')
                }, 2000)
            } catch (err) {
                this.error = err.response?.data?.detail || '注册失败，请稍后重试'
            } finally {
                this.loading = false
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

.register-container {
    min-height: 100vh;
    background: #fff;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 60px 16px;
}

.register-box {
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
    margin-top: 10px;
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

.success-message {
    color: #155724;
    font-size: 14px;
    margin-bottom: 15px;
    padding: 10px;
    background: #d4edda;
    border-radius: 4px;
}

.login-link {
    text-align: center;
    margin-top: 30px;
    font-size: 14px;
    color: #666;
}

.login-link a {
    color: #333;
    font-weight: 500;
    text-decoration: none;
}

.login-link a:hover {
    text-decoration: underline;
}

@media (max-width: 480px) {
    .register-container {
        padding: 40px 16px;
    }
}
</style>
