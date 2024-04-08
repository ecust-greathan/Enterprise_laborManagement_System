from django.db import models

class roles(models.Model):
    roleName = models.CharField(max_length=32)
    status_choice = (
        (0,'已禁用'),
        (1,'已启用')
    )
    status = models.SmallIntegerField(choices=status_choice,default=1)
    description = models.CharField(max_length=128,null=True,blank=True)
    permIds = models.JSONField(null=True, blank=True)