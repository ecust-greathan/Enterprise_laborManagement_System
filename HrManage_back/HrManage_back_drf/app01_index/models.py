from django.db import models
from app02_roles.models import roles
# Create your models here.

class user(models.Model):
    phone = models.CharField(verbose_name='手机号',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=32)
    token = models.CharField(verbose_name='凭证', max_length=64, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.id

class userInfo(models.Model):
    username = models.CharField(verbose_name='姓名', max_length=32)
    email = models.CharField(verbose_name='邮箱', max_length=32, null=True, blank=True)
    gender_choice = (
        (0, '男'),
        (1, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice, default=0)
    userId = models.ForeignKey(user, on_delete=models.CASCADE)
    status_choice = (
        (1,'正常'),
        (2,'禁用')
    )
    status = models.IntegerField(verbose_name='用户状态',choices=status_choice,default=1)

    role = models.ForeignKey(roles,verbose_name='用户角色',default=3,on_delete=models.CASCADE)  #和roles表的id进行外键连接

    moreDetail = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)

    mobile_num = models.CharField(max_length=32,blank=True,null=True)
    roles = models.JSONField(null=True, blank=True)

