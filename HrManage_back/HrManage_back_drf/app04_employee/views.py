from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app04_employee.models import employee
from app03_department.models import depart
from .serializer import EmployeeSerializer,EmployeeAddSerializer
from app01_index.utils import userPermissions
class employeeList(APIView):
    def get(self, request):
        # 获取查询参数
        print(request.query_params)
        department_id = request.query_params.get('departmentId')
        keyword = request.query_params.get('keyword', '')

        if (department_id == '8'):
            employees = employee.objects.all()
        else:
            employees = employee.objects.filter(departmentId=department_id)

        # 根据 keyword 进行模糊查询
        if keyword:
            employees = employees.filter(employeeName__icontains=keyword)

        # 序列化员工信息
        serializer = EmployeeSerializer(employees, many=True)

        # 构建返回数据
        response_data = {
            "success": True,
            "code": 1000,
            "data": {
                "total": employees.count(),
                "rows": serializer.data
            },
            "message": "员工信息获取成功"
        }

        return Response(response_data)

class employeeDelView(APIView):
    def delete(self, request, id):
        try:
            # 获取员工对象
            emp = employee.objects.get(phone_num=id)

            # 删除员工
            emp.delete()

            # 返回JSON格式数据
            content = {
                "success": True,
                "code": 1000,
                "data": None,
                "message": "员工删除成功"
            }

            return Response(content)
        except employee.DoesNotExist:
            # 如果员工不存在，返回404
            return Response({"message": "指定的员工不存在"}, status=status.HTTP_404_NOT_FOUND)


class EmployeeAddView(APIView):
    def post(self, request):
        # 获取前端传递的数据
        data = request.data
        depart_id = data.get('departmentId')
        depart_11 = depart.objects.get(id=depart_id)
        data['departmentName'] = depart_11.departName
        # 生成员工工号
        last_employee = employee.objects.last()
        if last_employee:
            last_work_number = last_employee.workNumber
            current_number = int(last_work_number.split('ECUST')[-1]) + 1
            new_work_number = f'ECUST{current_number:03d}'
        else:
            new_work_number = 'ECUST001'

        # 添加工号到数据中
        data['workNumber'] = new_work_number
        # 使用序列化器验证和保存员工信息
        serializer = EmployeeAddSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # 返回JSON格式数据
            response_data = {
                "success": True,
                "code": 1000,
                "data": {"id": serializer.data['phone_num']},
                "message": "员工添加成功"
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # 返回带有验证错误的错误响应
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    def get(self, request, id):
        try:
            # 获取员工对象
            emp = employee.objects.get(phone_num=id)

            # 序列化员工信息
            serializer = EmployeeAddSerializer(emp)

            # 构建返回数据
            response_data = {
                "success": True,
                "code": 1000,
                "data": serializer.data,
                "message": "员工详情获取成功"
            }

            return Response(response_data)
        except employee.DoesNotExist:
            # 如果员工不存在，返回404
            return Response({"message": "指定的员工不存在"}, status=status.HTTP_404_NOT_FOUND)

class EmployeeRoleAssignView(APIView):
    def put(self, request):
        try:
            # 从请求数据中获取员工id和角色id列表
            employee_id = request.data.get('id')
            role_ids = request.data.get('roleIds')

            # # 获取员工对象
            # emp = employee.objects.get(phone_num=employee_id)
            #
            # # 更新员工的roleIds字段
            # emp.roleIds = role_ids
            # emp.save()

            emp = userPermissions(phone_num=employee_id,role_ids=role_ids)

            # 序列化员工信息（如果需要返回更新后的员工信息）
            serializer = EmployeeSerializer(emp)
            # 构建返回数据
            response_data = {
                "success": True,
                "code": 1000,
                "data": serializer.data,
                "message": "员工角色分配成功"
            }

            return Response(response_data)

        except employee.DoesNotExist:
            # 如果员工不存在，返回404
            return Response({"message": "指定的员工不存在"}, status=status.HTTP_404_NOT_FOUND)

