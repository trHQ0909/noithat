from django.db import models

from customers.models import Customer
from django.core.validators import MinValueValidator, MaxValueValidator  # Thêm dòng này
class CategoryMain(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False  # Không cho Django tự động tạo bảng
        db_table = 'categorymain'  # Khớp với tên bảng trong CSDL
class Category(models.Model):
    categoryid = models.AutoField(db_column='categoryID', primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    main_category = models.ForeignKey(CategoryMain, on_delete=models.CASCADE, db_column="main_category_id", null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'category'  # Đã xóa `managed = False`

class Product(models.Model):
    productid = models.AutoField(db_column='productID', primary_key=True)
    name = models.CharField(max_length=255)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryID', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    sold = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    average_rating = models.FloatField(default=0.0)  # Điểm trung bình (1-5)
    total_reviews = models.PositiveIntegerField(default=0)  # Tổng số đánh giá
    class Meta:
        managed = False
        db_table = 'product'  # Đã xóa `managed = False`

# Model quản lý ảnh sản phẩm
class ProductImage(models.Model):
    imageid = models.AutoField(db_column='imageID', primary_key=True)
    productid = models.ForeignKey(Product, models.CASCADE, db_column='productID', related_name='images')
    image_url = models.CharField(max_length=255)  # Đường dẫn ảnh
    is_main = models.BooleanField(default=False)  # Ảnh chính (True) hay ảnh phụ (False)

    class Meta:
        managed = False
        db_table = 'product_image'
class ProductRating(models.Model):
    rating_id = models.AutoField(primary_key=True, db_column='rating_id')
    productid = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        db_column='productID',
        related_name='ratings'
    )
    customerid = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE,
        db_column='customerID',
        related_name='product_ratings'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],  # Thêm ràng buộc 1-5 sao
        blank=True, 
        null=True
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'product_ratings'    