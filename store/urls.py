from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"api/products", views.ProductViewSet)
router.register(r"api/categories", views.CategoryViewSet)


urlpatterns = [
    path("", views.store, name="store"),
    path("", include(router.urls)),
    path("product/<slug:product_slug>/", views.product_info, name="product-info"),
    path("search/<slug:category_slug>/", views.list_category, name="list-category"),
]
