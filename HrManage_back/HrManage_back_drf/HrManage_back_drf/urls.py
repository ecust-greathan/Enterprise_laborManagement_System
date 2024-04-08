"""
URL configuration for HrManage_back_drf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('app01_index.urls', 'app01_index'), namespace='index')),
    path('api/role/', include(('app02_roles.urls', 'app02_roles'), namespace='roles')),
    path('api/department/', include(('app03_department.urls', 'app03_department'), namespace='department')),
    path('api/employee/', include(('app04_employee.urls', 'app04_employee'), namespace='employee')),
    path('api/permission/', include(('app05_permission.urls', 'app05_permission'), namespace='permission')),
]
