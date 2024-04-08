from django.db import models

class permission(models.Model):
    name = models.CharField(max_length=32,verbose_name='权限名称')
    description = models.CharField(max_length=64,verbose_name='权限描述')
    type = models.IntegerField()
    code = models.CharField(max_length=32,verbose_name='权限标识符')
    pid = models.IntegerField() # 页面权限点pid值为'0', 按钮权限点值为所属页面权限点的id值

