from django.shortcuts import render

from .models import Category, Product

from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer

from django.contrib.auth.views import LoginView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def store(request):
    all_products = Product.objects.all()

    # Sorting products based on query parameters
    sort_by = request.GET.get("sort_by")
    if sort_by == "price_asc":
        all_products = all_products.order_by("price")
    elif sort_by == "price_desc":
        all_products = all_products.order_by("-price")
    elif sort_by == "name_asc":
        all_products = all_products.order_by("title")
    elif sort_by == "name_desc":
        all_products = all_products.order_by("-title")

    # Pagination
    paginator = Paginator(all_products, 10)  # Show 10 products per page
    page_number = request.GET.get("page")

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        "my_products": products,
        "sort_by": sort_by,
    }

    return render(request, "store/store.html", context)


def categories(request):
    all_categories = Category.objects.all()

    return {"all_categories": all_categories}


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {"product": product}

    return render(request, "store/product-info.html", context)


def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    # Sorting products based on query parameters
    sort_by = request.GET.get("sort_by")
    if sort_by == "price_asc":
        products = products.order_by("price")
    elif sort_by == "price_desc":
        products = products.order_by("-price")
    elif sort_by == "name_asc":
        products = products.order_by("title")
    elif sort_by == "name_desc":
        products = products.order_by("-title")

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get("page")
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        "category": category,
        "products": products,
        "sort_by": sort_by,
    }

    return render(request, "store/list-category.html", context)


# API
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
