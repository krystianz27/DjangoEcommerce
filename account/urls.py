from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register", views.register, name="register"),
    # Email verification
    path(
        "email-verification/<str:uidb64>/<str:token>/",
        views.email_verification,
        name="email-verification",
    ),
    path(
        "email-verification-sent",
        views.email_verification_sent,
        name="email-verification-sent",
    ),
    path(
        "email-verification-success",
        views.email_verification_success,
        name="email-verification-success",
    ),
    path(
        "email-verification-failed",
        views.email_verification_failed,
        name="email-verification-failed",
    ),
    # Login/Logout
    path("my-login", views.my_login, name="my-login"),
    path("user-logout", views.user_logout, name="user-logout"),
    #
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile-management", views.profile_management, name="profile-management"),
    path("delete-account", views.delete_account, name="delete-account"),
    # Password reset
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password-reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    # Manage shipping
    path("manage-shipping", views.manage_shipping, name="manage-shipping"),
    path("my-orders", views.my_orders, name="my-orders"),
    path("order/<int:order_id>", views.order_detail_view, name="order-detail"),
    # API AUTH
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
