from common.constants import Gender
from base.models import TimeStampedModel
from oauth.constants import AccountStatus
from oauth.models import User

from django.db import models
from oauth.models import Role  
from django.utils import timezone


def avatar_file(instance, filename):
    return  "\\".join(['employees', str(instance.id), filename])


class Employee(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    office = models.ForeignKey('hr.Office', on_delete=models.CASCADE, blank=True, related_name="employees",null=True)
    work_mail = models.EmailField(max_length=255, null=True)
    personal_mail = models.EmailField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.CHOICES, default=Gender.MALE, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_file, max_length=255, blank=True, null=True)
    join_date = models.DateField(default=timezone.now)
    roles = models.ManyToManyField(Role, related_name="employees", null=True, blank=True)
    status = models.SmallIntegerField(choices=AccountStatus.CHOICES, default=AccountStatus.DEACTIVE, blank=True)

    class Meta:
        db_table = "employees"

    @property
    def photo_value(self):
        return self.avatar

    @property
    def image_attr(self):
        return self.avatar
