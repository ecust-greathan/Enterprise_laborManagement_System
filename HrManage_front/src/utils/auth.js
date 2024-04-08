// 和localStorage一样，cookie也是一种存储数据的方式，但是cookie的优势在于可以设置过期时间，而且cookie的大小也比localStorage大。
import Cookies from 'js-cookie'

const TokenKey = 'vue_admin_template_token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
