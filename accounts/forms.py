from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

"""
Custom form classes used throughout the authentication system.

These extend Django's built-in forms so we can provide:
- Cleaner HTML structure for templates
- Custom widgets and placeholders
- HTML5 validation attributes
- Extra behaviour such as email-based login
"""


# ------------------------------------------------------------
# SIGNUP FORM
# ------------------------------------------------------------
class SignUpForm(UserCreationForm):
    """
    Extends Django's default signup form by:
    - Adding a required email field
    - Applying custom input attributes for better UX

    Django's default UserCreationForm does NOT save email by default,
    so we attach it manually in the save() override.
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
        Connects this form to Django’s built-in User model.
        Django automatically handles password hashing and validation.
        """
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        """
        Override save() to attach the email field to the user instance.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# ------------------------------------------------------------
# LOGIN FORM (USERNAME OR EMAIL)
# ------------------------------------------------------------
class EmailOrUsernameLoginForm(forms.Form):
    """
    Custom login form that accepts EITHER:
    - Username
    - Email address

    Validation checks:
    - User exists (by username OR email)
    - Password is correct

    If authentication succeeds, the authenticated user instance
    is stored in self.user for the view to log in.
    """

    identifier = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter username or email",
            "required": "required",
            "class": "form-control",
        })
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "required": "required",
            "class": "form-control",
        })
    )

    def clean(self):
        """
        Custom validation logic:
        - Look up user by username first
        - If not found, try email
        - Authenticate via Django’s auth backend
        - If invalid, raise a form-wide error
        """
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")

        # Find user by username OR email
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            user = User.objects.filter(email=identifier).first()

        if not user:
            raise forms.ValidationError(
                "No account found with that username or email."
            )

        # Authenticate using the *real* username
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is None:
            raise forms.ValidationError("Incorrect password. Please try again.")

        # Store authenticated user for the view
        self.user = authenticated_user
        return cleaned_data


# ------------------------------------------------------------
# CHANGE EMAIL FORM
# ------------------------------------------------------------
class ChangeEmailForm(forms.ModelForm):
    """
    Simple form allowing the user to update their email address.
    Includes HTML5 validation and clean placeholder text.
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


# ------------------------------------------------------------
# CHANGE USERNAME FORM
# ------------------------------------------------------------
class ChangeUsernameForm(forms.ModelForm):
    """
    Allows users to update their username.
    Includes:
    - Min/max length
    - Regex pattern for allowed characters

    This prevents invalid usernames from being saved.
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
