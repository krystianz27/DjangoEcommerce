from django.urls import path, include
from . import views


urlpatterns = [
    path("checkout", views.checkout, name="checkout"),
    path("complete-order", views.complete_order, name="complete-order"),
    path("payment-success", views.payment_success, name="payment-success"),
    path("payment-fail", views.payment_fail, name="payment-fail"),
]
