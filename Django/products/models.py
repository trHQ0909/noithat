from django.db import models

class Category(models.Model):
    categoryid = models.AutoField(db_column='categoryID', primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'  # Xóa `managed = False`

class Product(models.Model):
    productid = models.AutoField(db_column='productID', primary_key=True)
    name = models.CharField(max_length=255)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryID', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    sold = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'  # Xóa `managed = False`
