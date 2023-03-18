from django.db import models
from accounts.models import *
# Create your models here.


class ParkingPlace(models.Model):

    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=64, blank=True, null=True)
    address_line_1 = models.CharField(max_length=512, blank=True, null=True)
    address_line_2 = models.CharField(max_length=512, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=32, blank=True, null=True)
    pincode = models.CharField(max_length=8, blank=True, null=True)
    rate_per_hr = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ParkingTrack(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    parking_place = models.ForeignKey(ParkingPlace, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    rate_per_hr = models.IntegerField(default=0)
    approx_duration = models.IntegerField(default=0)
    final_duration = models.IntegerField(default=0)
    is_exited = models.BooleanField(default=False)
    vehicle_type = models.CharField(max_length=32, blank=True, null=True)
    vehicle_no = models.CharField(max_length=16, blank=True, null=True)
    # state => requested | accepted | rejected 
    state = models.CharField(max_length=16, blank=True, null=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)



