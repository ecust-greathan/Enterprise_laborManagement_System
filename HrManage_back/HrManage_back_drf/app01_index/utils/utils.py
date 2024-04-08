from app04_employee.models import employee
from app02_roles.models import roles
from app01_index.models import userInfo
from app05_permission.models import permission

def  userPermissions(phone_num,role_ids):
    # 获取用户
    user = employee.objects.get(phone_num=phone_num)
    # 更新角色信息
    user.roleIds = role_ids
    user.save()

    # 获取所有权限的permIds
    all_perms_ids = []
    for role_id in role_ids:
        role = roles.objects.get(id=role_id)
        all_perms_ids.extend(role.permIds)

    # 去重获取权限的pid列表
    unique_perm_pids = list(set(all_perms_ids)) # all_perms_ids，其中可能包含重复的元素。使用 set 和 list 函数，我们可以先将 all_perms_ids 转换为一个集合，这样重复的元素会被自动去除。然后，我们将这个集合转换回列表，从而得到一个去重的列表

    # 获取权限的code列表
    permission_codes = permission.objects.filter(id__in=unique_perm_pids).values_list('code', flat=True)
    permission_codes = list(permission_codes)
    print(permission_codes)
    # 获取用户信息
    user_info = userInfo.objects.get(mobile_num=phone_num)

    # 保存权限信息到userInfo表
    user_info.roles = permission_codes
    user_info.save()

    return user

