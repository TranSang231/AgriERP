from base.views import BaseViewSet
from hr.models import Unit
from hr.serializers.unit import (
    UnitSerializer,
    UnitTreeSerializer,
)
from base.utils.string import StringUtil
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from common.constants.http import Http
from businesses.models.employee import Employee
from businesses.serializers.employee import EmployeeShortSerializer
class UnitViewSet(BaseViewSet):
    queryset = Unit.objects.all()
    queryset_map = {
        "retrieve": Unit.objects.prefetch_related("members"),
    }
    serializer_class = UnitSerializer
    serializer_map = {
        "tree": UnitTreeSerializer,
    }
    
    required_alternate_scopes = {
        "create": [["organization:edit"]],
        "retrieve": [["organization:view"], ["organization:edit"]],
        "update": [["organization:edit"]],
        "add_member": [["organization:edit"]],
        "remove_member": [["organization:edit"]],
        "destroy": [["organization:edit"]],
        "list": [["organization:view"], ["organization:edit"]],
        "move": [["organization:edit"]],
        "tree": [["organization:view"], ["organization:edit"]]
    }

    @action(methods=[Http.HTTP_PUT], detail=True, url_path="add-member")
    def add_member(self, request, *args, **kwargs):
        data = request.data
        unit_id =StringUtil.get_id(data["unit_id"])
        employee_id =  StringUtil.get_id(data["employee_id"])
        employee = Employee.objects.get(pk=employee_id) if employee_id else None
        if employee:
            instance = self.get_object()
            if instance.members.filter(pk=employee.pk).exists():
                return Response({"detail": "Employee already exists in members."}, status=400)
            instance.members.add(employee)
            serializer = EmployeeShortSerializer(employee)
            return Response({"id": employee_id, "employee": serializer.data,"unit_id":unit_id})
        return Response({"error_message": 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=[Http.HTTP_DELETE], detail=True, url_path="remove-member")
    def remove_member(self, request, *args, **kwargs):
        data = request.data
        employee_id =  StringUtil.get_id(data["employee_id"])
        employee = Employee.objects.get(pk=employee_id) if employee_id else None
        if employee:
            instance = self.get_object()
            instance.members.remove(employee)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error_message": 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=[Http.HTTP_GET], detail=False)
    def tree(self, request, *args, **kwargs):
        query_set = self.get_queryset().filter(parent=None)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
     # @action(detail=False, methods=[HttpMethod.POST], url_path="import")
    # def import_data(self, request):
    #     data = request.data
    #     serializer = self.get_serializer(data=data, many=isinstance(data, list))
    #     if serializer.is_valid(raise_exception=True):
    #         self.perform_create(serializer)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @action(methods=[HttpMethod.PUT], detail=False)
    # def move(self, request, *args, **kwargs):
    #     data = request.data
    #     user_id =  Utils.get_id(data["user_id"])
    #     from_unit_id = Utils.get_id(data["from_unit_id"])
    #     to_unit_id = Utils.get_id(data["to_unit_id"])
    #     UnitService.move_member(user_id, from_unit_id, to_unit_id)
    #     return Response({"Success": True})