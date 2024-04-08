from django.urls import path
from .views import *

urlpatterns = [
    path('list/enabled', roleListView.as_view(), name='roleDetail'),  #获取已启用的角色，比如管理员、普通员工等
    path('addRole', roleAddView.as_view(), name='roleDetail'),  #添加角色
    path('updateRole/<str:pk>/', roleUpdateView.as_view(), name='update-role'), #修改角色信息
    path('roleDelete/<str:pk>/', roleDeleteView.as_view(), name='delete-role'),
    path('detail/<str:id>/', roleDetailView.as_view(), name='roleDetail'),  #获取角色详细信息
    path('assignPrem', rolePremView.as_view(), name='rolePrem'),  #更新角色权限信息
    path('NameList/enabled', roleNameListView.as_view()),
]