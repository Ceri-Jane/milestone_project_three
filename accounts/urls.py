# -------------------------------------------------------------
# Accounts URL Configuration
# -------------------------------------------------------------
# This file configures all authentication and user-account related
# routes for the project.
#
# Key updates:
# - Now uses *custom* login_view (email OR username support)
#   instead of Django’s LoginView, so that:
#       • errors display correctly
#       • email login works
#       • form.non_field_errors() is populated
#       • our LoginForm is used
#
# - Logout continues to use Django's LogoutView.
# - Added Django’s full password reset workflow (4 screens).
# -------------------------------------------------------------

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ---------------------------------------------------------
    # AUTHENTICATION (Custom Login / Django Logout)
    # ---------------------------------------------------------
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

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
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset-sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
