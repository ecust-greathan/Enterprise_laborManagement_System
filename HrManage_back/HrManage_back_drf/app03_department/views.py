from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import DepartSerializer,DepartAddSerializer
from .models import depart
from app01_index.models import userInfo

class departListView(APIView):
    def get(self,request):
        # 获取所有部门数据
        departments = depart.objects.all()

        # 序列化部门数据
        serializer = DepartSerializer(departments, many=True)

        # 返回JSON格式数据
        response_data = {
            "success": True,
            "code": 1000,
            "data": serializer.data,
            "message": "部门数据获取成功"
        }

        return Response(response_data,status=status.HTTP_200_OK)

class departAddView(APIView):
    def post(self, request):
        data = request.data.copy()
        manage_id = data.get('manageId')
        user_info = userInfo.objects.get(id=manage_id)
        data['manageName'] = user_info.username
        # 反序列化请求数据
        serializer = DepartAddSerializer(data=data)

        # 验证数据
        if serializer.is_valid():
            # 保存部门信息到数据库
            department = serializer.save()

            # 返回JSON格式数据
            response_data = {
                "success": True,
                "code": 0,
                "data": {"id": department.id},
                "message": "部门添加成功"
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # 返回带有验证错误的错误响应
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class departDetailView(APIView):
    def get(self, request, id):
        try:
            # 获取部门详情
            department = depart.objects.get(id=id)

            # 序列化部门详情数据
            serializer = DepartSerializer(department)

            # 返回JSON格式数据
            response_data = {
                "success": True,
                "code": 1000,
                "data": serializer.data,
                "message": "部门详情获取成功"
            }

            return Response(response_data)
        except depart.DoesNotExist:
            # 如果部门不存在，返回404
            return Response({"message": "指定的部门不存在"}, status=status.HTTP_404_NOT_FOUND)

class departUpdateView(APIView):
    def put(self, request, id):
        try:
            # 获取部门对象
            department = depart.objects.get(id=id)
            data = request.data.copy()
            manage_id = data.get('manageId')
            user_info = userInfo.objects.get(id=manage_id)
            data['manageName'] = user_info.username
            # 反序列化请求数据
            serializer = DepartAddSerializer(instance=department, data=data, partial=True)

            # 验证数据
            if serializer.is_valid():
                # 保存更新后的部门信息
                serializer.save()

                # 返回JSON格式数据
                response_data = {
                    "success": True,
                    "code": 0,
                    "data": '',
                    "message": "部门信息更新成功"
                }

                return Response(response_data)
            else:
                # 返回带有验证错误的错误响应
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except depart.DoesNotExist:
            # 如果部门不存在，返回404
            return Response({"message": "指定的部门不存在"}, status=status.HTTP_404_NOT_FOUND)


class departDeleteView(APIView):
    def delete(self, request, id):
        try:
            # 获取部门对象
            department = depart.objects.get(id=id)

            # 删除部门
            department.delete()

            # 返回JSON格式数据
            response_data = {
                "success": True,
                "code": 0,
                "data": None,
                "message": "部门删除成功"
            }

            return Response(response_data)
        except depart.DoesNotExist:
            # 如果部门不存在，返回404
            return Response({"message": "指定的部门不存在"}, status=status.HTTP_404_NOT_FOUND)