from django.db import models
from accounts.models import *

# Create your models here.



class PaymentMethod(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    stripe_payment_method_id = models.CharField(max_length=64, blank=True, null=True)
    stripe_payment_method_response = models.JSONField(max_length=512, blank=True, null=True)

    name_on_card = models.CharField(max_length=128, blank=True, null=True)
    ptype = models.CharField(max_length=32, blank=True, null=True)
    card_no = models.CharField(max_length=32, blank=True, null=True)
    exp_month = models.CharField(max_length=8, blank=True, null=True)
    exp_year = models.CharField(max_length=8, blank=True, null=True)
    cvv_no = models.CharField(max_length=8, blank=True, null=True)

    billing_address = models.TextField(max_length=512, blank=True, null=True)
    currency = models.CharField(max_length=16, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class PaymentHistory(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    payment_to = models.CharField(max_length=32, blank=True, null=True)
    payment_method = models.JSONField(max_length=1024, blank=True, null=True)
    payment_type = models.CharField(max_length=32, null=True, blank=True)
    currency = models.CharField(max_length=8,null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_response = models.JSONField(max_length=2000,null=True,blank=True)
    amount = models.FloatField(default=0, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ProviderWallet(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField(default=0)





