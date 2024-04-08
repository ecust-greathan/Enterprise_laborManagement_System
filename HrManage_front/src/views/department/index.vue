<template>
  <div class="container">
    <div class="app-container">
      <el-tree :expand-on-click-node="false" default-expand-all :data="depts" :props="defaultProps">
        <!-- 节点结构 -->
        <!-- v-slot="{ node, data }" 只能作用在template -->
        <template v-slot="{ data }">
          <el-row style="width:100%;height:40px" type="flex" justify="space-between" align="middle">
            <el-col>{{ data.departName }}</el-col>
            <el-col :span="4">
              <span class="tree-manager">{{ data.manageName }}</span>
              <!-- $event 实参 表示类型 后面还可以跟参数-->
              <el-dropdown @command="operateDept($event,data.id)">
                <!-- 显示区域内容 -->
                <span class="el-dropdown-link">
                  操作<i class="el-icon-arrow-down el-icon--right" />
                </span>
                <!-- 下拉菜单选项 -->
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="add">添加子部门</el-dropdown-item>
                  <el-dropdown-item command="edit">编辑部门</el-dropdown-item>
                  <el-dropdown-item command="del">删除</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </el-col>
          </el-row>
        </template>
      </el-tree>
    </div>
    <!-- 放置弹层组件 -->
    <AddDept ref="addDept" :current-node-id="currentNodeId" :show-dialog.sync="showDialog" @updateDepartment="getDepartment" />
  </div>
</template>
<script>
import { getDepartment, delDepartment } from '@/api/department'
import { transListToTreeData } from '@/utils'
import AddDept from './components/add-dept.vue'
export default {
  name: 'Department',
  components: {
    AddDept
  },
  data() {
    return {
      currentNodeId: '', // 当前节点id
      showDialog: false,
      depts: [{
        name: '传智教育',
        managerName: '管理员',
        children: [
          { departName: '总裁办', manageName: '张三' },
          { departName: '行政部', manageName: '李四' },
          { departName: '财务部', manageName: '王五' }
        ]
      }],
      defaultProps: {
        children: 'children',
        label: 'name'
      }
    }
  },
  created() {
    this.getDepartment() // 调用获取部门数据
  },
  methods: {
    // 获取部门数据
    async getDepartment() {
      const res = await getDepartment()
      this.depts = transListToTreeData(res, 0)
    },
    // 操作部门的方法
    operateDept(type, id) {
      if (type === 'add') {
        // 添加子部门
        this.showDialog = true
        this.currentNodeId = id
      } else if (type === 'edit') {
        this.showDialog = true
        this.currentNodeId = id // 传递当前节点id,要用它获取部门数据
        // 要在子组件中获取数据，父组件调用子组件方法获取数据
        this.$nextTick(() => { // 要等props更新完后再调用方法
          this.$refs.addDept.getDepartmentDetail()
        })
      } else {
        // 删除部门
        this.$confirm('您确认要删除该部门吗', '提示', { confirmButtonText: '确定', cancelButtonText: '取消' }).then(async() => {
          await delDepartment(id)
          // 提示消息
          this.$message.success('删除部门成功')
          this.getDepartment()
        })
      }
    }
  }
}
</script>

<style scoped>
.app-container {
  padding: 30px 140px;
  font-size: 14px;
}
.tree-manager {
  width: 50px;
  display: inline-block;
  margin: 10px;
  margin-right: 30px;
}
</style>

