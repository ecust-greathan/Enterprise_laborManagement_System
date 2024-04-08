from django.urls import path
from .views import *

urlpatterns = [
    path('List', employeeList.as_view(), name='employyList'),
    path('delete/<str:id>', employeeDelView.as_view(), name='employdel'),
    path('addEmployee', EmployeeAddView.as_view(), name='employee-add'),
    path('employeeInfo/<str:id>', EmployeeDetailView.as_view(), name='employee-detail'),
    path('rolesAssign', EmployeeRoleAssignView.as_view(), name='employee-detail'),
]