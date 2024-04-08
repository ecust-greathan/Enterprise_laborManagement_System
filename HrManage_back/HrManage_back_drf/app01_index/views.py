from rest_framework.views import APIView
from rest_framework.response import Response
from app01_index import models
from app01_index import serializer
import uuid
class LoginView(APIView):
    def post(self, request):
        # ser = request.data  #{phone,password}
        ser = serializer.LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1001, 'error': '校验失败', 'detail': ser.errors})
        instance = models.user.objects.filter(**ser.validated_data).first()
        if not instance:
            return Response({"code": 1002, 'error': '用户名或密码错误','message':'用户名或密码错误'})
        token = str(uuid.uuid4())
        instance.token = token
        instance.save()
        return Response({"message": "登录成功", "success": True, "code": 1000, 'data': token})

class UserInfoView(APIView):
    def get(self,request):
        authorization_header = request.headers.get('Authorization')  #从header中获取到token的值
        # 如果没有token，返回错误信息
        if not authorization_header:
            return Response({"error": "Authorization header is missing","code":1002}, status=400)
        # 在user表中查找具有特定token的用户
        # 提取token
        token = authorization_header.split(' ')[1] if authorization_header else None
        try:
            user_obj = models.user.objects.get(token=token)
        except models.user.DoesNotExist:
            return Response({"error": "User not found","code":1002}, status=404)

        # 在userInfo表中查找与用户关联的详细信息
        try:
            user_info_obj = models.userInfo.objects.get(userId=user_obj)
        except models.userInfo.DoesNotExist:
            return Response({"error": "User info not found"}, status=404)

        ser = serializer.UserInfoSerializer(instance=user_info_obj)
        # 构建响应数据
        content = {
            "success": True,
            "code": 1000,
            "data": ser.data,
            "message": "成功获取用户信息"
        }

        return Response(content)

class manageListView(APIView):
    def get(self,request):
        # 获取所有用户信息
        user_info_objs = models.userInfo.objects.all()
        # 创建序列化器
        ser = serializer.manageListSerializer(instance=user_info_objs, many=True)
        # 构建响应数据
        content = {
            "success": True,
            "code": 1000,
            "data": ser.data,
            "message": "成功获取负责人列表"
        }
        return Response(content)
