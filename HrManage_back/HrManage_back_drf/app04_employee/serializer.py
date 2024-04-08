from app04_employee.models import *
from rest_framework import serializers
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = ['phone_num', 'staffPhoto', 'employeeName', 'formOfEmployment', 'workNumber', 'departmentName', 'timeOfEntry','correctionTime']


class EmployeeAddSerializer(serializers.ModelSerializer):
    formatted_correction_time = serializers.DateTimeField(source='correctionTime', format='%Y-%m-%d', required=False)
    class Meta:
        model = employee
        fields = ['phone_num', 'employeeName', 'formOfEmployment', 'workNumber', 'departmentId', 'timeOfEntry','formatted_correction_time','departmentName','roleIds']



