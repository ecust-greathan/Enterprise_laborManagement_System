from rest_framework import serializers
from .models import roles
class RolesListSerializer(serializers.ModelSerializer):
    # status = serializers.ChoiceField(choices=roles.status_choice, source='get_status_display')
    class Meta:
        model = roles
        fields = ['id', 'roleName', 'status', 'description','permIds']

class RoleAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = roles
        fields = ['roleName', 'status', 'description']


class RolesDeatilSerializer(serializers.ModelSerializer):
    class Meta:
        model = roles
        fields = ['id', 'roleName', 'status', 'description','permIds']