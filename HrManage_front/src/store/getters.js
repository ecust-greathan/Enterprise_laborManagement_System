const getters = {
  sidebar: state => state.app.sidebar, // 取出app模块的sidebar的属性
  device: state => state.app.device,
  token: state => state.user.token,
  userId: state => state.user.userInfo.userId,
  avatar: state => state.user.userInfo.staffPhoto, // 头像
  name: state => state.user.userInfo.username, // 用户名
  roles: state => state.user.userInfo.roles
}
// getters方便我们在组件中使用，比如在组件中使用this.$store.getters.sidebar
export default getters
