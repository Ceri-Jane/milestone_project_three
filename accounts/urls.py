# -------------------------------------------------------------
# Accounts URL Configuration
# -------------------------------------------------------------
# This file was updated to align with the revised authentication
# structure used in this project.
#
# - The early prototype used custom login_view/logout_view,
#   but the final project uses Django’s built-in
#   LoginView and LogoutView for reliability, security,
#   and reduced boilerplate.
#
# - The signup, profile, change email, and change username
#   views are custom and imported from accounts.views.
#
# - LoginView is pointed to a custom template so it matches
#   the visual styling of the signup page.
#
# - This update resolves import errors where the old URLs
#   referenced non-existent view functions.
# -------------------------------------------------------------

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Django Auth Views (login/logout)
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Custom signup view
    path("signup/", views.signup, name="signup"),

    # Profile + user settings
    path("profile/", views.profile, name="profile"),
    path("change-email/", views.change_email, name="change_email"),
    path("change-username/", views.change_username, name="change_username"),
]
