from django.db import models
from accounts.models import Account

class Customer(models.Model):
    customerid = models.AutoField(db_column='customerID', primary_key=True)
    accountid = models.OneToOneField(Account, models.DO_NOTHING, db_column='accountID', blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'  # Xóa `managed = False`
