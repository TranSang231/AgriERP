from django.db import models
from base.models import TimeStampedModel
from businesses.models.employee import Employee
from .namespace import Namespace
class NamespaceMember(TimeStampedModel):
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE, related_name="namespace_memebers")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="namespace_memebers")

    class Meta:
        db_table = "knowledge_namespace_members"
