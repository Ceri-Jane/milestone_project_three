from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

"""
Custom form classes used for handling user authentication & profile updates.
These extend Django’s built-in forms so we can add:
- Extra fields (e.g. email during signup)
- Custom widgets for improved UI/UX
- HTML5 validation attributes
- More readable structure for templates
"""


class SignUpForm(UserCreationForm):
    """
    Extends Django's default signup form by adding a required email field.
    Django's built-in form does not save email by default, so this enforces it.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "required": "required",
            "type": "email",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        """
        Connect this form to the built-in User model.
        Django automatically handles password hashing and validation.
        """
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        """
        Override save() to attach the email field to the User instance.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Simple login form used with the custom EmailOrUsername backend.

    The 'identifier' field accepts either:
    - Username
    - Email address

    Password uses a PasswordInput widget so characters aren't visible.
    """
    identifier = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter username or email",
            "required": "required",
            "class": "form-control"
        })
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "required": "required",
            "class": "form-control"
        })
    )


class ChangeEmailForm(forms.ModelForm):
    """
    Form allowing the user to update their email.
    Includes HTML5 validation and placeholder text.
    """
    email = forms.EmailField(
        required=True,
        label="New Email",
        widget=forms.EmailInput(attrs={
            "required": "required",
            "type": "email",
            "placeholder": "Enter a valid email address"
        })
    )

    class Meta:
        model = User
        fields = ["email"]


class ChangeUsernameForm(forms.ModelForm):
    """
    Form allowing users to change their username.
    Uses regex + length constraints to enforce clean usernames.
    """
    username = forms.CharField(
        required=True,
        label="New Username",
        widget=forms.TextInput(attrs={
            "type": "text",
            "required": "required",
            "minlength": "3",
            "maxlength": "20",
            "pattern": "^[A-Za-z0-9_]{3,20}$",
            "title": "Username must be 3–20 characters and contain only letters, numbers, or underscores.",
            "placeholder": "Choose a username"
        })
    )

    class Meta:
        model = User
        fields = ["username"]
