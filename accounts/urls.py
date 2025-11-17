# -------------------------------------------------------------
# Accounts URL Configuration
# -------------------------------------------------------------
# This file configures all authentication and user-account related
# routes for the project.
#
# Key updates:
# - Uses Django's built-in LoginView + LogoutView for security,
#   session handling, and reduced boilerplate.
# - Custom views handle signup, profile, and account updates.
# - Added Django’s full password reset system (4-step workflow):
#     • password_reset                → user enters email
#     • password_reset_done           → “email sent” page
#     • password_reset_confirm        → user sets a new password
#     • password_reset_complete       → confirmation screen
#
# These are mapped to custom templates so the styling matches the
# signup/login pages already built.
# -------------------------------------------------------------

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ---------------------------------------------------------
    # AUTHENTICATION (Login / Logout)
    # ---------------------------------------------------------
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # ---------------------------------------------------------
    # SIGNUP (Custom)
    # ---------------------------------------------------------
    path("signup/", views.signup, name="signup"),

    # ---------------------------------------------------------
    # USER SETTINGS / PROFILE
    # ---------------------------------------------------------
    path("profile/", views.profile, name="profile"),
    path("change-email/", views.change_email, name="change_email"),
    path("change-username/", views.change_username, name="change_username"),

    # ---------------------------------------------------------
    # PASSWORD RESET WORKFLOW (Django built-in)
    # ---------------------------------------------------------
    # 1) Enter email
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),

    # 2) Email sent confirmation
    path(
        "password-reset-sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),

    # 3) Link from email → set new password
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    # 4) Final success page
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
