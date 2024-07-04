from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm, UpdateUserForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem

from django.contrib.auth.models import User, auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Email verification
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

# Markup email verification
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # Email verification setup
            current_site = get_current_site(request)
            email_subject = "Activate your account"
            message = render_to_string(
                "account/registration/email-verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": user_tokenizer_generate.make_token(user),
                },
            )
            # to_email = form.cleaned_data.get("email")
            # email = EmailMessage(email_subject, message, to=[to_email])
            # email.send()

            user.email_user(subject=email_subject, message=message)

            return redirect("email-verification-sent")

    context = {"form": form}

    return render(request, "account/registration/register.html", context)


def email_verification(request, uidb64, token):
    uniqie_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uniqie_id)

    # Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect("email-verification-success")

    # Failed
    else:
        return redirect("email-verification-failed")


def email_verification_sent(request):

    return render(request, "account/registration/email-verification-sent.html")


def email_verification_success(request):

    return render(request, "account/registration/email-verification-success.html")


def email_verification_failed(request):

    return render(request, "account/registration/email-verification-failed.html")


def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("dashboard")

    context = {"form": form}

    return render(request, "account/my-login.html", context)


def user_logout(request):

    # auth.logout(request)

    try:

        for key in list(request.session.keys()):

            if key == "session_key":
                continue
            else:
                del request.session[key]

    except KeyError:
        pass

    messages.info(request, "User logged out")

    return redirect("store")


@login_required(login_url="my-login")
def dashboard(request):

    return render(request, "account/dashboard.html")


@login_required(login_url="my-login")
def profile_management(request):
    form = UpdateUserForm(instance=request.user)

    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            messages.success(request, "Account updated")

            return redirect("dashboard")

    context = {"form": form}

    return render(request, "account/profile-management.html", context)


@login_required(login_url="my-login")
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        user.delete()
        # auth.logout(request)

        messages.error(request, "Account deleted successfully")

        return redirect("store")

    return render(request, "account/delete-account.html")


@login_required(login_url="my-login")
def manage_shipping(request):
    try:
        shipping = ShippingAddress.objects.get(user=request.user)

    except ShippingAddress.DoesNotExist:
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user

            shipping_user.save()

            messages.success(request, "Shipment details updated")

            return redirect("dashboard")

    context = {"form": form}

    return render(request, "account/manage-shipping.html", context)


@login_required(login_url="my-login")
def my_orders(request):
    orders_list = Order.objects.filter(user=request.user).order_by("-order_date")

    paginator = Paginator(orders_list, 10)

    page = request.GET.get("page")

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {"orders": orders}

    return render(request, "account/my-orders.html", context)


@login_required(login_url="my-login")
def order_detail_view(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
    except:
        return redirect("my-orders")

    context = {"order": order, "order_items": order_items}

    return render(request, "account/order-detail.html", context)
