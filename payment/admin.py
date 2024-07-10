from django.contrib import admin

from .models import ShippingAddress, Order, OrderItem

# Register your models here.


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "user",
        "email",
        "phone_number",
        "city",
    ]
    search_fields = [
        "id",
        "full_name",
        "user__username",
        "email",
        "phone_number",
        "city",
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "shipping_address",
        "paid_amount",
        "formatted_order_date",
        "user",
    ]

    list_filter = [
        "user",
    ]

    fields = [
        "full_name",
        "email",
        "shipping_address",
        "paid_amount",
        "user",
    ]

    search_fields = [
        "id",
        "full_name",
        "email",
        "shipping_address",
        "paid_amount",
        "order_date",
        "user__username",
    ]

    def formatted_order_date(self, obj):
        return obj.order_date.strftime("%d-%m-%Y %H:%M")

    formatted_order_date.short_description = "Order Date"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product",
        "quantity",
        "price",
    ]
    search_fields = [
        "id",
        "product__title",
        "quantity",
        "price",
    ]
