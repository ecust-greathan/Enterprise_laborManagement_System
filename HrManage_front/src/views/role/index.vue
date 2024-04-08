<template>
  <div class="container">
    <div class="app-container">
      <!-- 角色管理内容 -->
      <div class="role-operate">
        <el-button size="mini" type="primary" @click="showDialog = true">添加角色</el-button>
      </div>
      <!-- 放置table组件 他是父组件-->
      <el-table :data="list">
        <!-- 放置列 -->
        <el-table-column prop="roleName" align="center" width="300" label="角色">
          <template v-slot="{ row }">
            <!-- 条件判断 -->
            <el-input v-if="row.isEdit" v-model="row.editRow.roleName" size="mini" />
            <span v-else>{{ row.roleName }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" align="center" width="400" label="启用">
          <template v-slot="{ row }">
            <!-- 设置开关 “已启用为开” -->
            <el-switch v-if="row.isEdit" v-model="row.editRow.status" :active-value="1" :inactive-value="0" />
            <span v-else>  {{ row.status === 1 ? "已启用" : row.status === 0 ? "未启用" : "无" }} </span>
          </template>
        </el-table-column>
        <el-table-column prop="description" align="center" label="描述">
          <template v-slot="{ row }">
            <el-input v-if="row.isEdit" v-model="row.editRow.description" type="textarea" />
            <span v-else>{{ row.description }}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作">
          <template v-slot="{ row }">
            <template v-if="row.isEdit">
              <!-- 编辑状态 -->
              <el-button type="primary" size="mini" @click="btnEditOK(row)">确定</el-button>
              <el-button size="mini" @click="row.isEdit=false">取消</el-button>
            </template>
            <template v-else>
              <el-button type="text" @click="btnPermission(row.id)">分配权限</el-button>
              <el-button type="text" @click="btnEditRow(row)">编辑</el-button>
              <el-popconfirm title="确定要删除这一角色吗？" @onConfirm="confirmDel(row.id)">
                <el-button slot="reference" style="margin-left:10px" size="mini" type="text">删除</el-button>
              </el-popconfirm>
            </template>
          </template>
        </el-table-column>
      </el-table>
      <!-- 放置分页组件 -->
      <el-row type="flex" style="height:60px" align="middle" justify="end">
        <!-- 放置分页组件 -->
        <el-pagination
          :page-size="pageParams.pageSize"
          :current-page="pageParams.page"
          :total="pageParams.total"
          layout="prev, pager, next"
          @current-change="changePage"
        />
      </el-row>
    </div>
    <!-- 放置表单 -->
    <el-dialog width="500px" title="新增角色" :visible.sync="showDialog" @close="btnCancel">
      <!-- 表单内容  prop用于绑定校验，v-model用于绑定数据-->
      <el-form ref="roleForm" label-width="120px" :model="roleForm" :rules="rules">
        <el-form-item prop="roleName" label="角色名称">
          <el-input v-model="roleForm.roleName" style="width:300px" size="mini" />
        </el-form-item>
        <el-form-item prop="status" label="启用">
          <el-switch v-model="roleForm.status" :active-value="1" :inactive-value="0" size="mini" />
        </el-form-item>
        <el-form-item prop="description" label="角色描述">
          <el-input v-model="roleForm.description" type="textarea" :rows="3" style="width:300px" size="mini" />
        </el-form-item>
        <el-form-item>
          <el-row type="flex" justify="center">
            <el-col :span="16">
              <el-button type="primary" size="mini" @click="btnOK">确定</el-button>
              <el-button size="mini" @click="btnCancel">取消</el-button>
            </el-col>
          </el-row>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!-- 放置权限弹层 -->
    <el-dialog :visible.sync="showPermissionDialog" title="分配权限">
      <!-- 放置权限数据 -->
      <el-tree
        ref="permTree"
        node-key="id"
        :data="permissionData"
        :props="{ label: 'name' }"
        show-checkbox
        default-expand-all
        :default-checked-keys="permIds"
        check-strictly="true"
      />
      <el-row slot="footer" type="flex" justify="center">
        <el-col :span="6">
          <el-button type="primary" size="mini" @click="btnPermissionOK">确定</el-button>
          <el-button size="mini" @click="showPermissionDialog = false">取消</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>
<script>
import { getRoleList, addRole, updateRole, delRole, getRoleDetail, assignPerm } from '@/api/roles'
import { getPermissionList } from '@/api/permission'
import { transListToTreeData } from '@/utils'
export default {
  name: 'Role',
  data() {
    return {
      list: [],
      showDialog: false, // 是否显示新增用户的弹层
      // 将分页信息放在一个对象中
      pageParams: {
        page: 1, // 当前页
        pageSize: 5, // 每页显示的条数
        total: 0 // 总条数
      },
      roleForm: {
        roleName: '',
        description: '',
        status: 0 // 默认为1启用 关闭 0 打开1
      },
      rules: {
        roleName: [{ required: true, message: '角色名称不能为空', trigger: 'blur' }],
        description: [{ required: true, message: '角色描述不能为空', trigger: 'blur' }]
      },
      showPermissionDialog: false,
      permissionData: [],
      currentRoleId: null,
      permIds: []
    }
  },
  created() {
    this.getRoleList()
  },
  methods: {
    async getRoleList() {
      const { rows, total } = await getRoleList(this.pageParams)
      this.list = rows // 将返回的数据复制给list
      this.pageParams.total = total // 将返回的总条数赋值给分页对象
      // 针对每一行数据添加一个编辑标记
      this.list.forEach(item => {
        // item.isEdit = false // 添加一个属性 初始值为false
        // 数据响应式的问题  数据变化 视图更新
        // 添加的动态属性 不具备响应式特点
        // this.$set(目标对象, 属性名称, 初始值) 可以针对目标对象 添加的属性 添加响应式
        this.$set(item, 'isEdit', false)
        this.$set(item, 'editRow', {
          roleName: item.roleName,
          status: item.status,
          description: item.description
        })
      })
    },
    // 切换分页时 请求新的数据
    changePage(newPage) {
      this.pageParams.page = newPage // 赋值当前页码
      this.getRoleList()
    },
    btnOK() {
      this.$refs.roleForm.validate(async isOK => {
        if (isOK) {
          await addRole(this.roleForm)
          this.$message.success('添加角色成功')
          this.getRoleList() // 添加后刷新表单
          this.btnCancel()
        }
      })
    },
    btnCancel() {
      this.$refs.roleForm.resetFields() // 重置表单
      this.showDialog = false // 隐藏表单
    },
    // 点击编辑行
    btnEditRow(row) {
      row.isEdit = true // 改变行的编辑状态
      // 更新缓存数据
      row.editRow.roleName = row.roleName
      row.editRow.status = row.status
      row.editRow.description = row.description
    },
    // 点击确定时触发
    async  btnEditOK(row) {
      if (row.editRow.roleName && row.editRow.description) {
        // 下一步操作,更新数据延展editrow
        await updateRole({ ...row.editRow, id: row.id })
        // 更新成功
        this.$message.success('更新角色成功')
        // 更新显示数据  退出编辑状态
        // row.name = row.editRow.name // eslint的一校验 误判
        // Object.assign(target, source)  更新函数，将source的属性更新到target中
        Object.assign(row, {
          ...row.editRow,
          isEdit: false // 退出编辑模式
        }) // 规避eslint的误判
      } else {
        this.$message.warning('角色和描述不能为空')
      }
    },
    async  confirmDel(id) {
      await delRole(id) // 后端删除
      this.$message.success('删除角色成功')
      // 删除的如果是当前页的最后一个
      if (this.list.length === 1) this.pageParams.page--
      this.getRoleList()
    },
    async  btnPermission(id) {
      this.currentRoleId = id
      const result = await getRoleDetail(id)
      this.permIds = result.rows.permIds
      this.permissionData = transListToTreeData(await getPermissionList(), 0)
      this.showPermissionDialog = true
    },
    // 点击确定时触发
    async  btnPermissionOK() {
      await assignPerm({
        id: this.currentRoleId,
        permIds: this.$refs.permTree.getCheckedKeys()
      })
      this.$message.success('角色分配权限成功')
      this.showPermissionDialog = false
    }
  }
}

</script>

<style scoped>
.role-operate {
  padding: 10px;
}
</style>
