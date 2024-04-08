from django.urls import path
from .views import *

urlpatterns = [
    path('login', LoginView.as_view(), name='index'),
    path('user/profile', UserInfoView.as_view(), name='userInfo'),  #获取用户详细信息
    path('manageList', manageListView.as_view(), name='manageList'), #获取负责人列表
]