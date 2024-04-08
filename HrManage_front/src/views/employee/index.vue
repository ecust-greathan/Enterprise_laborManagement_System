<template>
  <div class="container">
    <div class="app-container">
      <div class="left">
        <el-input v-model="queryParams.keyword" style="margin-bottom:10px" type="text" prefix-icon="el-icon-search" size="small" placeholder="输入员工姓名全员搜索" @change="changeValue" />
        <!-- 树形组件 -->
        <el-tree
          ref="deptTree"
          node-key="id"
          :data="depts"
          :props="defaultProps"
          default-expand-all
          :expand-on-click-node="false"
          highlight-current
          @current-change="selectNode"
        />
      </div>
      <div class="right">
        <el-row class="opeate-tools" type="flex" justify="end">
          <el-button size="mini" type="primary" @click="$router.push('/employee/detail')">添加员工</el-button>
          <el-button size="mini">excel导入</el-button>
          <el-button size="mini">excel导出</el-button>
        </el-row>
        <!-- 表格组件 -->
        <el-table :data="List">
          <el-table-column prop="staffPhoto" align="center" label="头像">
            <el-table-column prop="staffPhoto" align="center" label="头像">
              <template v-slot="{ row }">
                <el-avatar v-if="row.staffPhoto" :src="row.staffPhoto" :size="30" />
                <span v-else class="username">{{ row.employeeName?.charAt(0) }}</span>
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column prop="employeeName" label="姓名" />
          <el-table-column prop="phone_num" label="手机号" sortable />
          <el-table-column prop="workNumber" label="工号" sortable />
          <el-table-column prop="formOfEmployment" label="聘用形式">
            <template v-slot="{ row }">
              <span v-if="row.formOfEmployment === 1">正式</span>
              <span v-else-if="row.formOfEmployment === 2">非正式</span>
              <span v-else>无</span>
            </template>
          </el-table-column>
          <el-table-column prop="departmentName" label="部门" />
          <el-table-column prop="timeOfEntry" label="入职时间" sortable />
          <el-table-column label="操作" width="280px">
            <template v-slot="{row}">
              <el-button size="mini" type="text" @click="$router.push(`/employee/detail/${row.phone_num}`)">查看</el-button>
              <el-button size="mini" type="text" @click="btnRole(row.phone_num)">角色</el-button>
              <el-popconfirm title="确认删除该员工吗？" @onConfirm="confirmDel(row.phone_num)">
                <el-button slot="reference" style="margin-left:10px" size="mini" type="text">删除</el-button>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页 -->
        <el-row style="height: 60px" align="middle" type="flex" justify="end">
          <el-pagination
            layout="total,prev, pager, next"
            :total="total"
            :current-page="queryParams.page"
            :page-size="queryParams.pagesize"
            @current-change="changePage"
          />
        </el-row>
      </div>
    </div>
    <el-dialog :visible.sync="showRoleDialog" title="分配角色">
      <!-- 弹层内容 -->
      <!-- checkbox -->
      <el-checkbox-group v-model="roleIds">
        <!-- 放置n个的checkbox  要执行checkbox的存储值 item.id-->
        <el-checkbox
          v-for="item in roleList"
          :key="item.id"
          :label="item.id"
        >{{ item.roleName }}</el-checkbox>
      </el-checkbox-group>
      <el-row slot="footer" type="flex" justify="center">
        <el-col :span="6">
          <el-button type="primary" size="mini" @click="btnRoleOK">确定</el-button>
          <el-button size="mini" @click="showRoleDialog = false">取消</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import { getDepartment } from '@/api/department'
import { transListToTreeData } from '@/utils/index'
import { getEmployeeList, delEmployee, getEnableRoleList, getEmployeeDetail, assignRole } from '@/api/employee'
export default {
  name: 'Employee',
  data() {
    return {
      depts: [], // 存储部门列表
      defaultProps: {
        children: 'children',
        label: 'departName'
      },
      // 存储查询参数
      queryParams: {
        departmentId: null,
        page: 1,
        pagesize: 10,
        keyword: '' // 模糊搜索字段
      },
      total: 0, // 员工总数
      List: [], // 存储员工信息列表
      showRoleDialog: false,
      roleList: [], // 存储角色列表
      roleIds: [], // 用来双向绑定数据的
      currentUserId: null // 当前点击的用户id
    }
  },
  created() {
    this.getDepartment()
  },
  methods: {
    async getDepartment() {
      // 递归方法 将列表转化成树形
      this.depts = transListToTreeData(await getDepartment(), 0)
      this.queryParams.departmentId = this.depts[0].id
      // 设置选中节点
      // 树组件渲染是异步的 等到更新完毕
      this.$nextTick(() => {
        // 此时意味着树渲染完毕
        this.$refs.deptTree.setCurrentKey(this.queryParams.departmentId)
      })
      // 这个时候的参数记录上了id
      this.getEmployeeList()
    },
    selectNode(node) {
      this.queryParams.departmentId = node.id
      this.queryParams.page = 1 // 切换部门时重置页码
      this.getEmployeeList()
    },
    async getEmployeeList() {
      const { rows, total } = await getEmployeeList(this.queryParams)
      this.List = rows
      this.total = total
    },
    // 切换页码时调用
    changePage(newPage) {
      this.queryParams.page = newPage
      this.getEmployeeList()
    },
    // 输入值内容改变时触发，失去焦点或按下enter
    changeValue() {
      this.queryParams.page = 1
      this.getEmployeeList()
    },
    // 删除员工
    async confirmDel(id) {
      await delEmployee(id)
      if (this.List.length === 1 && this.queryParams.page > 1) {
        this.queryParams.page--
      }
      this.getEmployeeList()
      this.$message.success('删除员工成功')
    },
    // 点击角色按钮弹出层
    async btnRole(phone_num) {
      const result = await getEnableRoleList()
      this.roleList = result.rows
      // 记录当前点击的id 因为后边 确定取消要存取给对应的用户
      this.currentUserId = phone_num
      const result1 = await getEmployeeDetail(phone_num)
      this.roleIds = result1.roleIds
      this.showRoleDialog = true
    },
    // 点击角色的确定
    async  btnRoleOK() {
      await assignRole({
        id: this.currentUserId,
        roleIds: this.roleIds
      })
      this.$message.success('分配用户角色成功')
      this.showRoleDialog = false
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  background: #fff;
  display: flex;
  .left {
    width: 280px;
    padding: 20px;
    border-right: 1px solid #eaeef4;
  }
  .right {
    flex: 1;
    padding: 20px;
    .opeate-tools {
      margin:10px ;
    }
    .username {
      height: 30px;
      width: 30px;
      line-height: 30px;
      text-align: center;
      border-radius: 50%;
      color: #fff;
      background: #04C9BE;
      font-size: 12px;
      display:inline-block;
    }
  }
}

</style>
