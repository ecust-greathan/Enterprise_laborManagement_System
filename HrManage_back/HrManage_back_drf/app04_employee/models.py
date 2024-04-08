from django.db import models
from app03_department.models import *

class employee(models.Model):
    phone_num = models.CharField(primary_key=True,max_length=32)
    employeeName = models.CharField(max_length=32)
    workNumber = models.CharField(max_length=32) # 工号
    timeOfEntry = models.DateField()
    departmentId = models.ForeignKey(depart,on_delete=models.CASCADE)
    departmentName = models.CharField(max_length=32,null=True,blank=True)
    form_choice = (
        (1,'正式'),
        (2,'非正式')
    )
    formOfEmployment = models.SmallIntegerField(choices=form_choice,default=1)
    staffPhoto = models.CharField(max_length=256,null=True,blank=True)
    correctionTime = models.DateField(null=True,blank=True)
    roleIds = models.JSONField(null=True,blank=True)


