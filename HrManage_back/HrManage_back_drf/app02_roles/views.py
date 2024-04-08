from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .serializer import RolesListSerializer,RoleAddSerializer,RolesDeatilSerializer
from app01_index.utils import updateUserPermissions
from .models import roles

class roleListView(APIView):
    def get(self,request):
        # 创建分页器实例
        paginator = PageNumberPagination()
        # 在视图中设置分页参数
        paginator.page_size = 5
        # 从数据库获取roles数据
        roles_data = roles.objects.all()
        # 使用分页器获取分页后的数据
        # 使用paginate_queryset方法时，它会自动从request.query_params中提取page参数，并使用该参数确定当前请求的页码，然后返回分页后的数据。
        page_roles = paginator.paginate_queryset(roles_data, request) # paginator是一个分页对象，它具有paginate_queryset方法，该方法接受两个参数：要分页的查询集和请求对象。这个方法会返回一个分页后的查询集以及与分页相关的其他数据，如当前页码、每页显示的项目数等。paginate_queryset方法的作用是将roles_data查询集按照指定的请求分页。分页时，它会考虑请求中的GET参数（如page和per_page）
        # 使用序列化器对roles数据进行序列化
        ser = RolesListSerializer(instance=page_roles, many=True)
        # 构建响应数据
        content = {
            "success": True,
            "code": 1000,
            "data": {
                'total':roles_data.count(),
                'rows':ser.data
            },
            "message": "成功获取角色信息"
        }
        return Response(content)

class roleAddView(APIView):
    def post(self,request):
        addRoleInfoSerializer = RoleAddSerializer(data=request.data)
        # 验证数据
        if addRoleInfoSerializer.is_valid():
            # 将角色保存到数据库
            addRoleInfoSerializer.save()
            # 响应数据
            content = {
                "success": True,
                "code": 1000,
                "message": "角色添加成功"
            }
            # 返回成功响应
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            # 返回带有验证错误的错误响应
            return Response(addRoleInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class roleUpdateView(APIView):
    def put(self,request,pk):
        # 获取角色对象
        try:
            role_instance = roles.objects.get(pk=pk)
        except roles.DoesNotExist:
            return Response({"message": "角色不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 反序列化请求数据，partial=True表示可以部分更新
        serializer = RoleAddSerializer(instance=role_instance, data=request.data, partial=True) # instance参数表示要更新的角色实例（如果存在）。data参数包含客户端发送的请求数据，partial参数设置为True表示可以部分更新角色对象

        # 验证数据
        if serializer.is_valid():
            # 保存更新后的角色信息
            serializer.save()
            # 构建返回信息
            content = {
                "success": True,
                "code": 1000,
                "data": '',
                "message": "角色更新成功"
            }
            # 返回成功响应
            return Response(content, status=status.HTTP_200_OK)
        else:
            # 返回带有验证错误的错误响应
            return Response({"message": "角色更新失败"}, status=status.HTTP_400_BAD_REQUEST)

class roleDeleteView(APIView):
    def delete(self,request,pk):
        # 获取角色对象
        try:
            role_instance = roles.objects.filter(pk=pk).order_by('id').first() # 删除时注意要对queryset进行排序，Django REST framework的分页器在处理无序的查询集（QuerySet）时可能导致结果不一致
        except roles.DoesNotExist:
            return Response({"message": "角色不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 删除角色
        role_instance.delete()

        # 构建返回信息
        content = {
            "success": True,
            "code": 1000,
            "data": '',
            "message": "角色删除成功"
        }
        # 返回成功响应
        return Response(content, status=status.HTTP_200_OK)


class roleNameListView(APIView):
    def get(self,request):
        # 从数据库获取roles数据
        roles_data = roles.objects.filter(status=1)

        # 使用序列化器对roles数据进行序列化
        ser = RolesListSerializer(instance=roles_data, many=True)
        # 构建响应数据
        content = {
            "success": True,
            "code": 1000,
            "data": {
                'total':roles_data.count(),
                'rows':ser.data
            },
            "message": "成功获取角色信息"
        }
        return Response(content)

class roleDetailView(APIView):
    def get(self,request,id):
        # 从数据库获取roles数据
        roles_data = roles.objects.filter(status=1)
        roles_data = roles.objects.get(id = id)
        # 使用序列化器对roles数据进行序列化
        ser = RolesDeatilSerializer(instance=roles_data)
        # 构建响应数据
        content = {
            "success": True,
            "code": 1000,
            "data": {
                'rows':ser.data
            },
            "message": "成功获取角色信息"
        }
        return Response(content)

class rolePremView(APIView):
    def put(self, request):
        try:
            # 从请求数据中获取角色id和权限id列表
            role_id = request.data.get('id')
            role_prems = request.data.get('permIds')

            # 获取角色对象
            role = roles.objects.get(id=role_id)

            # 更新角色的premId字段
            role.permIds = role_prems
            role.save()
            updateUserPermissions()
            # 构建返回数据
            response_data = {
                "success": True,
                "code": 1000,
                "data": '',
                "message": "角色权限分配成功"
            }

            return Response(response_data)

        except roles.DoesNotExist:
            # 如果员工不存在，返回404
            return Response({"message": "指定的角色不存在"}, status=status.HTTP_404_NOT_FOUND)