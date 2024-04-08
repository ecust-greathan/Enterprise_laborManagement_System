import request from '@/utils/request'

/** *
 * 获取角色列表
 * **/
export function getRoleList(params) {
  return request({
    url: '/role/list/enabled',
    params // 查询参数(分页参数)
  })
}

/** **
 * 新增角色
 * ***/
export function addRole(data) {
  return request({
    url: '/role/addRole',
    method: 'post',
    data
  })
}

/**
 * 更新角色
 * ***/
export function updateRole(data) {
  return request({
    url: `/role/updateRole/${data.id}/`,
    method: 'put',
    data
  })
}

/** *
 * 删除角色
 * **/

export function delRole(id) {
  return request({
    url: `/role/roleDelete/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取角色详情
 * **/

export function getRoleDetail(id) {
  return request({
    url: `/role/detail/${id}/`
  })
}

/**
 * 给角色分配权限
 *
 * ***/

export function assignPerm(data) {
  return request({
    url: '/role/assignPrem',
    method: 'put',
    data
  })
}
