import request from '@/utils/request'

/**
 *
 * 获取组织架构数据
 *
*/
export function getDepartment() {
  return request({
    url: '/department/departList'
  })
}

/**
 *
 *  获取部门负责人的数据
 * **/

export function getManagerList() {
  return request({
    url: '/manageList'
  })
}

/**
 * 新增部门
 * ***/
export function addDepartment(data) {
  return request({
    method: 'post',
    url: '/department/departAdd',
    data
  })
}

/**
 * 获取部门详情
 *
 * ***/

export function getDepartmentDetail(id) {
  return request({
    url: `/department/detail/${id}`
  })
}

/** *
 * 更新部门
 * ***/
export function updateDepartment(data) {
  return request({
    method: 'put',
    url: `/department/departUpdate/${data.id}`,
    data
  })
}

/**
 * 删除部门
 *
*/

export function delDepartment(id) {
  return request({
    method: 'delete',
    url: `/department/departDel/${id}`
  })
}
