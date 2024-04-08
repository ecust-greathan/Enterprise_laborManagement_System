from app05_permission.models import *
from rest_framework import serializers
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = permission
        fields = ['id', 'name', 'description', 'type', 'code', 'pid']


class PermissionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = permission
        fields = ['name', 'description', 'type', 'code', 'pid']




