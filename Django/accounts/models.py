from django.db import models

class Account(models.Model):
    accountid = models.AutoField(db_column='accountID', primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=100)
    role = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'  # Xóa `managed = False`
