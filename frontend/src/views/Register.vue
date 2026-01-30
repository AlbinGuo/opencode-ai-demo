<template>
    <div class="register-container">
        <div class="register-box">
            <h1>注册</h1>
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
.register-container {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
}

.register-box {
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
}

h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 8px;
    color: #666;
    font-size: 14px;
}

input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s;
}

input:focus {
    outline: none;
    border-color: #007bff;
}

button {
    width: 100%;
    padding: 12px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 10px;
}

button:hover:not(:disabled) {
    background-color: #218838;
}

button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.error-message {
    color: #dc3545;
    font-size: 14px;
    margin-bottom: 15px;
    padding: 10px;
    background-color: #f8d7da;
    border-radius: 4px;
}

.success-message {
    color: #155724;
    font-size: 14px;
    margin-bottom: 15px;
    padding: 10px;
    background-color: #d4edda;
    border-radius: 4px;
}

.login-link {
    text-align: center;
    margin-top: 20px;
    color: #666;
    font-size: 14px;
}

.login-link a {
    color: #007bff;
    text-decoration: none;
}

.login-link a:hover {
    text-decoration: underline;
}
</style>
