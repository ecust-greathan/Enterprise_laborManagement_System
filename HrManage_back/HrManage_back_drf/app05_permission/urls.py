from django.urls import path
from .views import *

urlpatterns = [
    path('list', permissionList.as_view(), name='permissionList'),
    path('add', PermissionAddView.as_view(), name='add_permission'),
    path('detail/<int:id>', PermissionDetailView.as_view(), name='get_permission_detail'),
    path('update/<int:id>', PermissionUpdateView.as_view(), name='update_permission'),
    path('delete/<int:id>', PermissionDeleteView.as_view(), name='delete_permission'),
]