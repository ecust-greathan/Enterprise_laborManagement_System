import axios from 'axios'
import store from '@/store'
import { Message } from 'element-ui'
import router from '@/router'

// 创建一个axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // 基地址 (环境区分 Day2.6)
  timeout: 10000, // 超时时间
  headers: {
    'Content-Type': 'application/json' // Set the content type header
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 注入token  store.getters.token,放到请求头中
    if (store.getters.token) {
      config.headers['Authorization'] = `Bearer ${store.getters.token}` // 格式参考接口文档
    }
    return config
  },
  error => {
    // 请求失败执行promise的reject方法
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 对响应数据进行处理
    const { data, message, success } = response.data // axios默认包括了一个data
    if (success) {
      return data
    } else {
      Message({ type: 'error', message: message, duration: 3 * 1000 })
      return Promise.reject(new Error(message))
    }
  },
  async error => {
    if (error.response.status === 401) {
      Message({ type: 'warning', message: 'token超时', duration: 3 * 1000 })
      // token超时
      await store.dispatch('user/logout') // 调用action退出登录
      // 跳转到登录页
      router.push('/login')
      return Promise.reject(error)
    }
    // 对响应错误进行处理
    Message({ type: 'error', message: error.message, duration: 3 * 1000 })
    return Promise.reject(error)
  }
)

export default service
