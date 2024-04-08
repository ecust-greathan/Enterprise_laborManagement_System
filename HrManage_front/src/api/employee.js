import request from '@/utils/request'

export function getEmployeeList(params) {
  return request({
    url: '/employee/List',
    params // 地址参数 查询参数
  })
}

/**
 * 删除员工
 * **/

export function delEmployee(id) {
  return request({
    method: 'delete',
    url: `/employee/delete/${id}`
  })
}

// 新增员工
export function addEmployee(data) {
  return request({
    url: '/employee/addEmployee',
    method: 'post',
    data
  })
}

/**
 *  获取员工详情
 * **/
export function getEmployeeDetail(id) {
  return request({
    url: `/employee/employeeInfo/${id}`
  })
}

/**
 * 分配角色时获取可用的角色
 * **/
export function getEnableRoleList() {
  return request({
    url: '/role/NameList/enabled'
  })
}

/**
 * 分配员工角色
 * ***/

export function assignRole(data) {
  return request({
    url: '/employee/rolesAssign',
    method: 'put',
    data
  })
}
