from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import (
    SignUpForm,
    LoginForm,
    ChangeEmailForm,
    ChangeUsernameForm,
)

"""
Views used for user authentication and account management.

Includes:
- Login (email OR username)
- Signup
- Profile view
- Change username
- Change email

These views rely on Django’s built-in authentication system,
plus a custom authentication backend which allows logging in with email.
"""


def login_view(request):
    """
    Handles user login using a custom authentication backend.
    Users can log in using either:
    - Username
    - Email address

    GET  → show blank login form
    POST → validate credentials, authenticate user, redirect home
    """
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data["password"]

            # Custom backend will accept email OR username
            user = authenticate(request, username=identifier, password=password)

            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid username/email or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def signup(request):
    """
    Handles user registration.
    GET  → show form
    POST → validate & create account, then redirect to login page.
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
    Basic profile page showing logged-in user info.
    Protected with @login_required.
    """
    return render(request, "accounts/profile.html")


@login_required
def change_email(request):
    """
    Allows logged-in users to update their email address.
    Updates the User model directly.
    """
    if request.method == "POST":
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Email updated successfully ✅")
            return redirect("profile")
    else:
        form = ChangeEmailForm(instance=request.user)

    return render(request, "accounts/change_email.html", {"form": form})


@login_required
def change_username(request):
    """
    Allows users to update their username.
    Includes regex validation from the form to prevent invalid characters.
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
