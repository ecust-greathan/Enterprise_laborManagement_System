from django.db import models
from app01_index.models import userInfo

class depart(models.Model):
    pid = models.IntegerField(null=True,blank=True)
    departName = models.CharField(max_length=32)
    departCode = models.CharField(max_length=32)
    manageId = models.ForeignKey('app01_index.userInfo', to_field='id', on_delete=models.CASCADE)
    manageName = models.CharField(max_length=32)
    introduce = models.CharField(max_length=255)
