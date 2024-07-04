from django.test import TestCase, Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from django.test import RequestFactory
from django.urls import reverse
from django.http import HttpRequest

from store.models import Product, Category
from cart.cart import Cart

from decimal import Decimal


# class CartUnitTests(TestCase):

#     def setUp(self):
#         self.factory = RequestFactory()
#         self.request = self.factory.get("/")
#         self.middleware = SessionMiddleware(lambda x: None)
#         self.middleware.process_request(self.request)
#         self.request.session.save()

#     def test_add_to_cart_new_product(self):
#         product = Product.objects.create(title="Test Product", price="10.00")

#         cart = Cart(self.request)
#         cart.add(product, 1)

#         self.assertEqual(len(cart), 1)
#         self.assertEqual(cart.get_total(), 10.00)

#     def test_add_to_cart_existing_product(self):
#         product = Product.objects.create(title="Test Product", price="10.00")

#         cart = Cart(self.request)
#         cart.add(product, 1)
#         cart.add(product, 2)

#         self.assertEqual(len(cart), 3)
#         self.assertEqual(cart.get_total(), 30.00)

#     def test_update_cart(self):
#         product = Product.objects.create(title="Test Product", price="10.00")

#         cart = Cart(self.request)
#         cart.add(product, 1)
#         cart.update(product.id, 3)

#         self.assertEqual(len(cart), 3)
#         self.assertEqual(cart.get_total(), 30.00)

#     def test_remove_from_cart(self):
#         product = Product.objects.create(title="Test Product", price="10.00")

#         cart = Cart(self.request)
#         cart.add(product, 1)
#         cart.delete(product.id)

#         self.assertEqual(len(cart), 0)
#         self.assertEqual(cart.get_total(), 0)

# def test_clear_cart(self):
#     product1 = Product.objects.create(title="Test Product 1", price="10.00")
#     product2 = Product.objects.create(title="Test Product 2", price="20.00")

#     cart = Cart(self.request)
#     cart.add(product1, 1)
#     cart.add(product2, 2)

#     self.assertEqual(len(cart), 2)
#     self.assertEqual(cart.get_total(), 50.00)

#     cart.clear()

#     self.assertEqual(len(cart), 0)
#     self.assertEqual(cart.get_total(), 0)


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.product = Product.objects.create(
            category=self.category,
            title="Test Product",
            brand="Test Brand",
            description="Test Description",
            price=50.00,
            image="default.jpg",
        )
        self.cart_add_url = reverse("cart-add")
        self.cart_delete_url = reverse("cart-delete")
        self.cart_update_url = reverse("cart-update")
        self.cart_summary_url = reverse("cart-summary")

    def get_request_with_session(self):
        """Helper method to create a request with a session"""
        request = RequestFactory().get("/")
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_add_to_cart(self):
        response = self.client.post(
            self.cart_add_url,
            {"product_id": self.product.id, "product_quantity": 1, "action": "post"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["qty"], 1)

    def test_update_cart(self):
        self.client.post(
            self.cart_add_url,
            {"product_id": self.product.id, "product_quantity": 1, "action": "post"},
        )
        response = self.client.post(
            self.cart_update_url,
            {"product_id": self.product.id, "product_quantity": 3, "action": "post"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["qty"], 3)

    def test_delete_from_cart(self):
        self.client.post(
            self.cart_add_url,
            {"product_id": self.product.id, "product_quantity": 1, "action": "post"},
        )
        response = self.client.post(
            self.cart_delete_url, {"product_id": self.product.id, "action": "post"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["qty"], 0)

    def test_cart_total(self):
        request = self.get_request_with_session()
        cart = Cart(request)
        cart.add(self.product, 2)
        total = cart.get_total()
        self.assertEqual(total, Decimal("100.00"))

    def test_cart_length(self):
        request = self.get_request_with_session()
        cart = Cart(request)
        cart.add(self.product, 2)
        self.assertEqual(len(cart), 2)

    def test_cart_iter(self):
        request = self.get_request_with_session()
        cart = Cart(request)
        cart.add(self.product, 2)
        items = list(cart)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["product"], self.product)
        self.assertEqual(items[0]["qty"], 2)
        self.assertEqual(items[0]["price"], Decimal("50.00"))
        self.assertEqual(items[0]["total"], Decimal("100.00"))
