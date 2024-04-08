from django.urls import path
from .views import *

urlpatterns = [
    path('departList', departListView.as_view(), name='departList'),  #获取已启用的角色，比如管理员、普通员工等
    path('departAdd', departAddView.as_view(), name='departAdd'),  # 添加部门
    path('detail/<str:id>/', departDetailView.as_view(), name='detail'),  # 获取部门详细信息
    path('departUpdate/<int:id>', departUpdateView.as_view(), name='departUpdate'),  # 更新部门信息
    path('departDel/<int:id>/', departDeleteView.as_view(), name='department-delete'),
]