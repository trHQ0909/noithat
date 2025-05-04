from django.test import TestCase
from products.models import Category, Product
from products.services import *

class ProductServiceTest(TestCase):

    def setUp(self):
        """Tạo dữ liệu mẫu trước khi test"""
        self.category = create_category("Bàn ghế", "Nội thất bàn ghế")
        self.product = create_product("Bàn gỗ", self.category.categoryid, 500000, "Bàn gỗ cao cấp", stock=10)

    def test_create_category(self):
        """Test tạo danh mục"""
        category = create_category("Ghế sofa", "Nội thất sofa")
        self.assertIsNotNone(category)
        self.assertEqual(category.name, "Ghế sofa")

    def test_get_category_by_id(self):
        """Test lấy danh mục theo ID"""
        category = get_category_by_id(self.category.categoryid)
        self.assertEqual(category.name, "Bàn ghế")

    def test_update_category(self):
        """Test cập nhật danh mục"""
        updated_category = update_category(self.category.categoryid, name="Bàn ghế VIP")
        self.assertEqual(updated_category.name, "Bàn ghế VIP")

    def test_delete_category(self):
        """Test xóa danh mục"""
        delete_category(self.category.categoryid)
        self.assertIsNone(get_category_by_id(self.category.categoryid))

    def test_create_product(self):
        """Test tạo sản phẩm"""
        product = create_product("Ghế gỗ", self.category.categoryid, 300000)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Ghế gỗ")

    def test_update_product(self):
        """Test cập nhật sản phẩm"""
        updated_product = update_product(self.product.productid, price=600000)
        self.assertEqual(updated_product.price, 600000)

    def test_delete_product(self):
        """Test xóa sản phẩm"""
        delete_product(self.product.productid)
        self.assertIsNone(get_product_by_id(self.product.productid))
