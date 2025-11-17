from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import (
    SignUpForm,
    EmailOrUsernameLoginForm,
    ChangeEmailForm,
    ChangeUsernameForm,
)

"""
Views for authentication and account management.

Includes:
- Login via username OR email
- Signup
- Profile page
- Change username
- Change email
"""


def login_view(request):
    """
    Handles login using the custom EmailOrUsernameLoginForm.
    - Accepts username OR email
    - Validates user existence + password
    - Uses form.user (set in form.clean()) to complete login
    """

    if request.method == "POST":
        form = EmailOrUsernameLoginForm(request.POST)

        if form.is_valid():
            # Retrieve authenticated user stored during form.clean()
            user = form.user
            login(request, user)
            return redirect("home")

        # If form is NOT valid, errors appear in form.non_field_errors()

    else:
        form = EmailOrUsernameLoginForm()

    return render(request, "accounts/login.html", {"form": form})


def signup(request):
    """
    Standard signup flow using custom SignUpForm.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! Please log in.")
            return redirect("login")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    """
    Basic profile page for authenticated users.
    """
    return render(request, "accounts/profile.html")


@login_required
def change_email(request):
    """
    Allows users to update their email address.
    """
    if request.method == "POST":
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Email updated successfully.")
            return redirect("profile")
    else:
        form = ChangeEmailForm(instance=request.user)

    return render(request, "accounts/change_email.html", {"form": form})


@login_required
def change_username(request):
    """
    Allows users to update their username.
    """
    if request.method == "POST":
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Username updated!")
            return redirect("profile")
    else:
        form = ChangeUsernameForm(instance=request.user)

    return render(request, "accounts/change_username.html", {"form": form})
