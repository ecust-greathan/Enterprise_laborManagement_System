import router from './router'
import store from './store'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { Message } from 'element-ui'
// import { asyncRoutes } from '@/router'
// 路由守卫配置文件
NProgress.configure({ showSpinner: false }) // NProgress Configuration

// 路由前置守卫
// router.beforeEach(async(to, from, next) => {
//   // start progress bar
//   NProgress.start()

//   // set page title
//   document.title = getPageTitle(to.meta.title)

//   // determine whether the user has logged in
//   const hasToken = getToken()

//   if (hasToken) {
//     if (to.path === '/login') {
//       // if is logged in, redirect to the home page
//       next({ path: '/' })
//       NProgress.done()
//     } else {
//       const hasGetUserInfo = store.getters.name
//       if (hasGetUserInfo) {
//         next()
//       } else {
//         try {
//           // get user info
//           await store.dispatch('user/getInfo')

//           next()
//         } catch (error) {
//           // remove token and go to login page to re-login
//           await store.dispatch('user/resetToken')
//           Message.error(error || 'Has Error')
//           next(`/login?redirect=${to.path}`)
//           NProgress.done()
//         }
//       }
//     }
//   } else {
//     /* has no token*/

//     if (whiteList.indexOf(to.path) !== -1) {
//       // in the free login whitelist, go directly
//       next()
//     } else {
//       // other pages that do not have permission to access are redirected to the login page.
//       next(`/login?redirect=${to.path}`)
//       NProgress.done()
//     }
//   }
// })

const whiteList = ['/login', '/404']
router.beforeEach(async(to, from, next) => {
  NProgress.start() // 页面上方的进度条
  if (store.getters.token) {
    // 存在token
    if (to.path === '/login') {
      // 跳转到主页
      next('/') // 中转到主页
      // next（地址）并没有执行后置守卫
      NProgress.done()
    } else {
      // 判断是否获取过用户信息
      if (!store.getters.userId) {
        await store.dispatch('user/getUserInfo') // 没有用户信息就获取用户信息
      }

      if (to.path === '/dashboard') {
        next()
      } else {
        // 检查用户是否有权限访问当前页面
        const allowedPages = store.getters.roles
        console.log(allowedPages)
        if (allowedPages.includes(to.name)) {
          next() // 放行
        } else {
          Message.error('您无权访问此页面')// 无权限，弹出提示
          NProgress.done()
        }
      }
    }
  } else {
    // 没有token
    if (whiteList.includes(to.path)) {
      next()
    } else {
      next('/login') // 中转到登录页
      NProgress.done()
    }
  }
})

// 路由后置守卫
router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
