import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
})

api.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            localStorage.removeItem('user')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export const login = async (username, password) => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    const response = await api.post('/api/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    const token = response.data.access_token
    localStorage.setItem('token', token)
    const userResponse = await api.get('/api/auth/me')
    localStorage.setItem('user', JSON.stringify(userResponse.data))
    return response.data
}

export const register = async (username, email, password) => {
    const response = await api.post('/api/auth/register', { username, email, password })
    return response.data
}

export const getCurrentUser = async () => {
    const response = await api.get('/api/auth/me')
    return response.data
}

export const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
}

export const setToken = (token) => {
    localStorage.setItem('token', token)
}

export const getToken = () => {
    return localStorage.getItem('token')
}

export const isAuthenticated = () => {
    return !!getToken()
}

export const giteeLogin = async () => {
    const response = await api.get('/api/auth/gitee')
    if (response.data.auth_url) {
        window.location.href = response.data.auth_url
    }
    return response.data
}

export const handleGiteeCallback = (token, avatarUrl = '') => {
    if (token) {
        setToken(token)
        localStorage.setItem('user', JSON.stringify({ 
            login_type: 'gitee',
            avatar_url: avatarUrl 
        }))
        return true
    }
    return false
}

export default api
