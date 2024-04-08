<template>
  <div class="login-container">
    <div class="logo" />
    <div class="form">
      <h1>登录</h1>
      <el-card shadow="never" class="login-card">
        <!--登录表单-->
        <el-form ref="form" :model="loginForm" :rules="loginRules">
          <el-form-item prop="mobile">  <!--prop 属性用于指定一个表单项的字段名。这个字段名将被用于表单验证  elementui特有的，在你给出的代码 <el-form-item prop="mobile"> 中，prop="mobile" 表示这个表单项对应的是 "mobile" 字段。当进行表单验证时，Element UI 将会查找并应用与 "mobile" 字段相关的验证规则。-->
            <el-input v-model="loginForm.phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="loginForm.password" show-password placeholder="请输入密码" /> <!--show-password 密码模式，属性用于指定是否显示密码切换按钮。-->
          </el-form-item>
          <el-form-item prop="isAgree">
            <el-checkbox v-model="loginForm.isAgree"> 用户平台使用协议 </el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-button style="width: 350px" type="primary" @click="login">登录</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        phone: '',
        password: '',
        isAgree: false
      },
      loginRules: {
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[34578]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '密码长度在6-20个字符', trigger: 'blur' }
        ],
        isAgree: [
          {
            // 自定义校验规则
            // rules是校验规则，value是当前表单项的值，callback是校验结果的回调函数，执行callback()表示校验通过，执行callback(new Error('错误信息'))表示校验不通过
            validator: (rule, value, callback) => {
              if (value) {
                callback()
              } else {
                callback(new Error('请同意用户平台使用协议'))
              }
            },
            trigger: 'change'
          }
        ]
      }
    }
  },
  methods: {
    login() {
      this.$refs.form.validate(async(isOK) => {
        if (isOK) {
          // this.$message.success('校验成功')   // validate 是一个方法，用于触发表单的验证。它接受一个回调函数作为参数，这个回调函数将在验证结束后被调用，并且会传入一个 boolean 类型的参数 isOK，这个参数表示了表单验证的结果。如果表单验证通过，isOK 的值为 true，否则为 false。
          // ref 是一个特殊的属性，用于在 Vue 组件中注册一个引用信息.你就可以在 Vue 组件的方法中通过 this.$refs.form 访问到这个 <el-form> 组件，然后调用它的方法或访问它的数据。例如，你可以使用 this.$refs.form.validate() 来触发表单的验证，或者使用 this.$refs.form.resetFields() 来重置表单的所有字段。
          await this.$store.dispatch('user/login', this.loginForm) // 加上await说明必须等待异步函数执行成功了，才会执行下面的代码
          // 跳转主页
          this.$router.push('/')
        }
      })
    }
  }
}
</script>
<style lang="scss">
.login-container {
  display: flex;
  align-items: stretch;
  height: 100vh;
  .logo {
    flex: 3;
    background: rgba(38, 72, 176) url(../../assets/common/login_back.png)
      no-repeat center / cover;
    border-top-right-radius: 60px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
    padding: 0 100px;
    .icon {
      background: url(../../assets/common/logo.png) no-repeat 70px center /
        contain;
      width: 300px;
      height: 50px;
      margin-bottom: 50px;
    }
    p {
      color: #fff;
      font-size: 18px;
      margin-top: 20px;
      width: 300px;
      text-align: center;
    }
  }
  .form {
    flex: 2;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 176px;
    .el-card {
      border: none;
      padding: 0;
    }
    h1 {
      padding-left: 20px;
      font-size: 24px;
    }
    .el-input {
      width: 350px;
      height: 44px;
      .el-input__inner {
        background: #f4f5fb;
      }
    }
    .el-checkbox {
      color: #606266;
    }
  }
}
</style>
