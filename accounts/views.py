from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SignUpForm, ChangeEmailForm, ChangeUsernameForm

"""
Views used for user account management:
- Sign up
- View profile
- Change username/email

These use Django’s built-in authentication system and custom forms.
"""

@login_required
def profile(request):
    """
    Basic profile page.
    Only available to logged-in users (protected with @login_required).
    """
    return render(request, "accounts/profile.html")


def signup(request):
    """
    Handles registration of new users.
    GET  → Show blank signup form
    POST → Validate submitted form, create account, redirect to login
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
def change_email(request):
    """
    Allows a logged-in user to update their email address.
    Saves the new email directly onto the user instance.
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
    Allows logged-in users to change their username.
    Uses form validation rules to prevent invalid characters.
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
