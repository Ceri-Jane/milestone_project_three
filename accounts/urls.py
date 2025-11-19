# -------------------------------------------------------------
# Accounts URL Configuration
# -------------------------------------------------------------
# Handles authentication, signup, profile management,
# password reset, and user account settings.
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
    # USER SETTINGS / PROFILE (User must already be logged in)
    # ---------------------------------------------------------
    path("profile/", views.profile, name="profile"),
    path("change-email/", views.change_email, name="change_email"),
    path("change-username/", views.change_username, name="change_username"),

    # ---------------------------------------------------------
    # PASSWORD CHANGE (User must already be logged in)
    # ---------------------------------------------------------
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password_form.html",
            success_url="/accounts/password-change-done/",
        ),
        name="password_change",
    ),
    path(
        "password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/change_password_done.html"
        ),
        name="password_change_done",
    ),

    # ---------------------------------------------------------
    # PASSWORD RESET WORKFLOW (Forgot password – not logged in)
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
