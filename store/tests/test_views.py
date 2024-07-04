from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from store.models import Category, Product


class ProductDetailViewTest(TestCase):
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

    def test_product_info_view(self):
        """Test Product Info view using Django's test client."""
        url = reverse("product-info", kwargs={"product_slug": self.product.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
        self.assertContains(response, "Lenovo")
        self.assertContains(response, "A powerful laptop")
        self.assertContains(response, "999.99")

        self.assertTemplateUsed(response, "store/product-info.html")

    def test_product_info_view_not_found(self):
        """Test Product Info view for non-existent product."""
        url = reverse("product-info", kwargs={"product_slug": "non-existent-slug"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)
