from django.db import models
from common.constants import Gender
from oauth.constants import AccountStatus
from base.models import TimeStampedModel
from oauth.models import User


class Customer(TimeStampedModel):
    email = models.EmailField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)  # Added address field
    avatar = models.TextField(blank=True, null=True)
    # Store VN administrative codes from external API
    province_id = models.CharField(max_length=64, blank=True, null=True)
    district_id = models.CharField(max_length=64, blank=True, null=True)
    ward_id = models.CharField(max_length=64, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=20, choices=Gender.CHOICES, default=Gender.MALE, blank=True, null=True)
    user = models.ForeignKey(User, related_name="customers", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.SmallIntegerField(choices=AccountStatus.CHOICES, default=AccountStatus.DEACTIVE, blank=True)


    class Meta:
        db_table = "ecommerce_customers"

    def __str__(self):
        return self.last_name
    
