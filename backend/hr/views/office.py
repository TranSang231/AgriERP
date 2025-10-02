from django.db.models import Q
from base.views import BaseViewSet
from ..models import Office
from ..serializers import OfficeSerializer
from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import action
from common.constants.http import Http
from base.utils.string import StringUtil
from businesses.models.employee import Employee
from businesses.serializers.employee import EmployeeShortSerializer

class OfficeViewSet(BaseViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    search_map ={
        "address": "icontains",
        "manager__first_name": "icontains",
        "manager__last_name": "icontains",
        "phone": "icontains",
    }
    required_alternate_scopes = {
        "create": [["offices:edit"]],
        "retrieve": [["offices:view"], ["offices:edit"]],
        "update": [["offices:edit"]],
        "destroy": [["offices:edit"]],
        "list": [["offices:view"], ["offices:edit"]],
        "tree": [["offices:view"], ["offices:edit"]],
        "add_employee": [["offices:edit"]],
        "remove_employee": [["offices:edit"]],
        "multiple_remove_employee": [["offices:edit"]],
        "all_employees": [["offices:edit"], ["offices:view"]],
    }

        
    def get_queryset(self):
        group_id = self.kwargs.get('group_pk')
        if group_id:
            return super().get_queryset().filter(group_id=group_id)
        else:
            return super().get_queryset()
        

    @action(methods=["put"], detail=True, url_path="employees/add-employees")
    def add_employee(self, request, *args, **kwargs):
        data = request.data
        employee_ids = data.get("ids", [])
        employees = []

        for emp_id in employee_ids:
            employee_id = StringUtil.get_id(emp_id)
            try:
                employee = Employee.objects.get(pk=employee_id)
                employees.append(employee)
            except Employee.DoesNotExist:
                return Response(
                    {"error_message": f'Employee with ID {emp_id} not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        instance = self.get_object()
        instance.employees.add(*employees)

        serializer = EmployeeShortSerializer(employees, many=True)
        return Response({"office_id": kwargs["pk"], "employees": serializer.data})
    
    @action(methods=[Http.HTTP_DELETE], detail=True, url_path="employees/(?P<employee_id>[^/.]+)")
    def remove_employee(self, request, *args, **kwargs):
        employee_id = kwargs.get("employee_id")
        employee = Employee.objects.get(pk=employee_id) if employee_id else None
        if employee:
            instance = self.get_object()
            instance.employees.remove(employee)
            serializer = EmployeeShortSerializer(employee)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error_message": 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=[Http.HTTP_DELETE], detail=True, url_path="employees/remove-employees")
    def multiple_remove_employee(self, request, *args, **kwargs):
        data = request.data
        employee_ids = data.get("ids", [])
        
        # Get all employees with employee_ids
        employees = Employee.objects.filter(pk__in=employee_ids)

        #Check if any employee does not exist
        if len(employees) != len(employee_ids):
            not_found_ids = set(employee_ids) - set(employees.values_list('pk', flat=True))
            return Response(
                {"error_message": f'Employees with IDs {list(not_found_ids)} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete employees from instance
        instance = self.get_object()
        instance.employees.remove(*employees)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=True, url_path="employees")
    def all_employees(self, request, *args, **kwargs):
        search = {
            "first_name": "icontains",
            "work_mail": "icontains"
        }
        office_id = kwargs["pk"] 
        employees = Employee.objects.filter(office_id=office_id)

        params = request.query_params
        keyword = params.get("keyword")

        if keyword and len(search) > 0:
            query = Q()
            for field, op in search.items():
                kwargs = {'{0}__{1}'.format(field, op): keyword}
                query |= Q(**kwargs)
            employees = employees.filter(query)

        if params.get('page_size') is not None:
            page = self.paginate_queryset(employees)
            data = EmployeeShortSerializer(page, many=True).data
            return self.get_paginated_response(data)
        else:
            data = EmployeeShortSerializer(employees, many=True).data
            return Response(data, status=status.HTTP_200_OK)
