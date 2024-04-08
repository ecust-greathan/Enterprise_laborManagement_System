from rest_framework import serializers
from app01_index import models
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.user
        fields = ["phone","password"]

class UserInfoSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=models.userInfo.gender_choice, source='get_gender_display')
    status = serializers.ChoiceField(choices=models.userInfo.status_choice, source='get_status_display')
    # role = serializers.ChoiceField(choices=models.userInfo.role_choice, source='get_role_display')
    role = serializers.StringRelatedField(source='role.roleName')  # 使用 StringRelatedField 显示外键的字符串表示形式
    class Meta:
        model = models.userInfo
        fields = ['username', 'email', 'gender', 'userId', 'status', 'role', 'moreDetail','mobile_num','roles']


class manageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.userInfo
        fields = ["id","username"]