<template>
  <el-dialog :title="showTitle" :visible="showDialog" @close="close">
    <!-- 放置弹层内容 -->
    <!-- label-width="120px 让label对齐 -->
    <el-form ref="addDept" label-width="120px" :model="formData" :rules="rules">
      <el-form-item prop="departName" label="部门名称">
        <el-input v-model="formData.departName" placeholder="2-10个字符" style="width: 80%" size="mini" />
      </el-form-item>
      <el-form-item v-model="departCode" label="部门编码" prop="code">
        <el-input v-model="formData.departCode" placeholder="2-10个字符" style="width: 80%" size="mini" />
      </el-form-item>
      <el-form-item label="部门负责人" prop="manageId">
        <el-select v-model="formData.manageId" placeholder="请选择负责人" style="width: 80%" size="mini">
          <!-- 下拉选项 循环负责人数据-->
          <el-option
            v-for="item in managerList"
            :key="item.id"
            :label="item.username"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="部门介绍" prop="introduce">
        <el-input v-model="formData.introduce" placeholder="1-100个字符" type="textarea" size="mini" :rows="4" style="width: 80%" />
      </el-form-item>
      <el-form-item>
        <!-- 按钮 -->
        <el-row type="flex" justify="center">
          <el-col :span="12">
            <el-button size="mini" type="primary" @click="btnOK">确定</el-button>
            <el-button size="mini" @click="close">取消</el-button>
          </el-col>
        </el-row>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
import { getDepartment, getManagerList, addDepartment, getDepartmentDetail, updateDepartment } from '@/api/department'
export default {
  name: 'AddDept',
  props: {
    showDialog: {
      type: Boolean,
      default: false
    },
    currentNodeId: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      managerList: [], // 存储部门负责人列表
      formData: {
        departCode: '', // 部门编码
        introduce: '', // 部门介绍
        manageId: '', // 部门负责人
        departName: '', // 部门名称
        pid: '' // 父级部门
      },
      rules: {
        departCode: [{ required: true, message: '部门编码不能为空', trigger: 'blur' },
          {
            min: 2, max: 10, message: '部门编码的长度为2-10个字符', trigger: 'blur'
          },
          {
            // 校验code是否和数据库中的code有重复
            trigger: 'blur',
            validator: async(rule, value, callback) => {
              let result = await getDepartment()
              if (this.formData.id) {
                // 编辑场景，排除自身
                result = result.filter(item => item.id !== this.formData.id)
              }
              if (result.some(item => item.departCode === value)) { // .some() 方法接收一个回调函数作为参数，这个回调函数会被数组的每个元素调用，直到找到一个使回调函数返回 true 的元素。如果找到了这样的元素，.some() 方法将立即返回 true。如果数组中的所有元素都没有使回调函数返回 true，那么 .some() 方法将返回 false。
                callback(new Error('部门编码已存在'))
              } else {
                callback()
              }
            }
          }
        ], // 部门编码
        introduce: [{ required: true, message: '部门介绍不能为空', trigger: 'blur' }, {
          min: 1, max: 100, message: '部门介绍的长度为1-100个字符', trigger: 'blur'
        }
        ], // 部门介绍
        managerId: [{ required: true, message: '部门负责人不能为空', trigger: 'blur' }], // 部门负责人id
        departName: [{ required: true, message: '部门名称不能为空', trigger: 'blur' },
          {
            min: 2, max: 10, message: '部门名称的长度为2-10个字符', trigger: 'blur'
          },
          {
          // 校验部门名称是否和数据库中的编码有重复
            trigger: 'blur',
            validator: async(rule, value, callback) => {
              let result = await getDepartment()
              if (this.formData.id) {
                // 编辑场景，排除自身
                result = result.filter(item => item.id !== this.formData.id)
              }
              if (result.some(item => item.departName === value)) {
                callback(new Error('部门名称已存在'))
              } else {
                callback()
              }
            }
          }
        ] // 部门名称
        // pid: '' // 父级部门的id 不需要做校验
      }
    }
  },
  computed: {
    showTitle() {
      return this.formData.id ? '编辑部门' : '新增部门'
    }
  },
  async created() {
    // 获取部门负责人
    this.getManagerList()
  },
  methods: {
    close() {
      this.formData = {
        departCode: '', // 部门编码
        introduce: '', // 部门介绍
        manageId: '', // 部门负责人
        departName: '', // 部门名称
        pid: '' // 父级部门
      }
      this.$refs.addDept.resetFields() // 重置表单
      this.$emit('update:showDialog', false)
    },
    async getManagerList() {
      // 获取部门负责人
      const res = await getManagerList()
      this.managerList = res
    },
    // 点击确定时调用
    btnOK() {
      this.$refs.addDept.validate(async isOK => {
        if (isOK) {
          // 通过formdata中是否有id来判断是新增还是编辑
          if (this.formData.id) {
            // 编辑部门
            await updateDepartment(this.formData)
            this.$message.success(`编辑部门成功`)
          } else {
            await addDepartment({ ...this.formData, pid: this.currentNodeId }) // ...this.formData 对formData进行了一次复制又加入了pid，组成一个新的对象
            this.$message.success(`新增部门成功`)
          }
          // 通知父组件更新
          this.$emit('updateDepartment')
          // 提示消息

          this.close()
        }
      })
    },
    async getDepartmentDetail() {
      const res = await getDepartmentDetail(this.currentNodeId)
      this.formData = res
    }
  }
}
</script>
