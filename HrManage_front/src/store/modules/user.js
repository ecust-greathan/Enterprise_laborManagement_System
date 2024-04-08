import { getToken, setToken, removeToken } from '@/utils/auth'
import { login, getUserInfo } from '@/api/user'
import { Message } from 'element-ui'
const state = {
  // Define your state properties here
  token: getToken(), // 应该要从缓存中获取token
  userInfo: {} // 用户信息
}

const getters = {
  // Define your getters here
}

// vuex中的数据修改只能通过mutations中的方法修改
const mutations = {
  // Define your mutations here
  settoken(state, token) {
    state.token = token
    // 同步到缓存
    setToken(token)
  },
  removetoken(state) {
    // 清空vuex的token
    state.token = ''
    // 清空缓存的token
    removeToken()
  },
  // 设置用户信息
  setUserInfo(state, userInfo) {
    state.userInfo = userInfo
  }

}

const actions = {
  // Define your actions here
  // 第一个参数是context，后面是传递的参数
  async login(context, data) {
    console.log(data)
    // 调用登录接口（后面写）
    const token = await login(data)
    Message({ type: 'success', message: '登录成功', duration: 3 * 1000 })
    // 返回token保存到vuex
    context.commit('settoken', token)
  },
  // 获取用户基本信息
  async getUserInfo(context) {
    // 调用获取用户信息接口
    const result = await getUserInfo()
    context.commit('setUserInfo', result)
    return result
  },
  // 退出登录的action
  async logout(context) {
    // 清空token
    context.commit('removetoken')
    // 清空用户信息
    context.commit('setUserInfo', {})
  }
}

export default {
  namespaced: true, // 开启命名空间，后面调用方法的时候就带上user名称
  state,
  getters,
  mutations,
  actions
}
