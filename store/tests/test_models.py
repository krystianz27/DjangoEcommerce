from django.test import TestCase
from django.utils.text import slugify
from store.models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            category=self.category,
            title="Laptop",
            brand="Lenovo",
            description="A powerful laptop",
            price=999.99,
            default_image="media/images/default.jpg",
        )

    def test_product_creation(self):
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.title, "Laptop")
        self.assertEqual(self.product.brand, "Lenovo")
        self.assertEqual(self.product.description, "A powerful laptop")
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.default_image, "media/images/default.jpg")

    def test_product_slug_generation(self):
        self.assertEqual(self.product.slug, slugify(self.product.title))

    def test_product_str(self):
        self.assertEqual(str(self.product), "Laptop")

    def test_product_default_brand(self):
        product_without_brand = Product.objects.create(
            category=self.category,
            title="Mouse",
            price=29.99,
            default_image="media/images/default.jpg",
        )
        self.assertEqual(product_without_brand.brand, "unbranded")
