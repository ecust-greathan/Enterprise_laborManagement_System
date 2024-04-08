from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app05_permission.models import permission
from app05_permission.serializer import PermissionSerializer,PermissionAddSerializer

class permissionList(APIView):
    def get(self, request):
        # 获取所有权限信息
        permissions = permission.objects.all()

        # 序列化权限信息
        serializer = PermissionSerializer(permissions, many=True)

        # 构建返回数据
        response_data = {
            "success": True,
            "code": 1000,
            "data": serializer.data,
            "message": "权限列表获取成功"
        }

        return Response(response_data)

class PermissionAddView(APIView):
    def post(self, request):
        serializer = PermissionAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                "success": True,
                "code": 1000,
                "data": serializer.data,
                "message": "权限添加成功"
            }
            return Response(content,status=status.HTTP_201_CREATED)
        return Response({'success': False, 'code': 1, 'data': None, 'message': 'Failed to add permission.',
                         'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PermissionDetailView(APIView):
    def get(self, request, id):
        try:
            permission_detail = permission.objects.get(id=id)
            serializer = PermissionSerializer(permission_detail)
            content = {
                "success": True,
                "code": 1000,
                "data": serializer.data,
                "message": "权限信息获取成功"
            }
            return Response(content)
        except permission.DoesNotExist:
            return Response({'success': False, 'code': 1, 'data': None, 'message': 'Permission not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class PermissionUpdateView(APIView):
    def put(self, request, id):
        try:
            permission_find = permission.objects.get(id=id)
            serializer = PermissionSerializer(permission_find, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                content = {
                    "success": True,
                    "code": 1000,
                    "data": '',
                    "message": "权限信息更新成功"
                }
                return Response(content)
            return Response({'success': False, 'code': 1, 'data': None, 'message': 'Failed to update permission.',
                             'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except permission.DoesNotExist:
            return Response({'success': False, 'code': 2, 'data': None, 'message': 'Permission not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class PermissionDeleteView(APIView):
    def delete(self, request, id):
        try:
            permission_del = permission.objects.get(id=id)
            permission_del.delete()
            return Response({'success': True, 'code': 0, 'data': None, 'message': 'Permission deleted successfully.'})
        except permission.DoesNotExist:
            return Response({'success': False, 'code': 1, 'data': None, 'message': 'Permission not found.'},
                            status=status.HTTP_404_NOT_FOUND)



