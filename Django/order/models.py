from django.db import models
from customers.models import Customer
from products.models import Product

class Order(models.Model):
    orderid = models.AutoField(db_column='orderID', primary_key=True)
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customerID', blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    payment_method = models.CharField(max_length=13, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'  # Xóa `managed = False`

class OrderDetail(models.Model):
    orderdetailid = models.AutoField(db_column='orderdetailID', primary_key=True)
    orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='orderID', blank=True, null=True)
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='productID', blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orderdetail'  # Xóa `managed = False`
