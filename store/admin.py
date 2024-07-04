from django.contrib import admin
from .models import Category, Product, ProductPhoto


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = [
        "id",
        "name",
    ]


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1


admin.site.register(ProductPhoto)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPhotoInline]
    list_filter = ("category",)
    list_display = [
        "id",
        "title",
        "brand",
        "price",
    ]
