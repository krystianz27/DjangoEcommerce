import requests

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.core.mail import send_mail

from django.conf import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse

# Create your views here.


@login_required(login_url="my-login")
def checkout(request):

    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user)

            context = {"shipping_address": shipping_address}

            return render(request, "payment/checkout.html", context)

        except ShippingAddress.DoesNotExist:
            return render(request, "payment/checkout.html")

    else:
        # Guest user
        return render(request, "payment/checkout.html")


@login_required(login_url="my-login")
def complete_order(request):
    if request.POST.get("action") == "post":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        shipping_address = f"{address1}\n{address2}\n{city}\n{state}\n{zipcode}"

        cart = Cart(request)
        total_cost = cart.get_total()
        product_list = []

        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                paid_amount=total_cost,
            )
        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                paid_amount=total_cost,
            )

        order_id = order.pk

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["qty"],
                price=item["price"],
            )
            product_list.append(item["product"])

        send_order_confirmation_email(order)

        order_success = True
        response = JsonResponse({"success": order_success, "order_id": order_id})
        return response


def send_order_confirmation_email(order):
    subject = "Order Confirmation - Order #{}".format(order.pk)
    template = "payment/order-confirmation.html"

    context = {
        "order": order,
    }

    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)

    recipient_email = order.email

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        html_message=html_message,
        fail_silently=False,
    )


@login_required(login_url="my-login")
def payment_success(request):
    order_id = request.GET.get("order_id")

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return HttpResponse(
            "Order not found. Please check your order details or contact support.",
            status=404,
        )

    for key in list(request.session.keys()):

        if key == "session_key":
            del request.session[key]

    context = {"order_id": order_id, "email": order.email}

    return render(request, "payment/payment-success.html", context)


@login_required(login_url="my-login")
def payment_fail(request):

    return render(request, "payment/payment-failed.html")
