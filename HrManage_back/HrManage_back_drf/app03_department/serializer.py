from rest_framework import serializers
from .models import depart
from app01_index.models import userInfo

class DepartSerializer(serializers.ModelSerializer):
    class Meta:
        model = depart
        fields = ['id', 'pid', 'departName', 'departCode', 'manageId', 'manageName', 'introduce']

class DepartAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = depart
        fields = ['pid', 'departName', 'departCode', 'manageId', 'manageName', 'introduce']

