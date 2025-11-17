from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

"""
Custom forms for user account creation and updates.
These extend Django’s default authentication forms so we can collect
extra fields (like email) and apply our own validation + UI attributes.
"""

class SignUpForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm:
    - Adds a required email field
    - Customises widgets for accessible placeholders + HTML5 validation
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
        These are the fields required to create an account.
        """
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        """
        Override save() so we can attach the email field to the user object.
        Django’s default form does NOT save email, so we add it here.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ChangeEmailForm(forms.ModelForm):
    """
    Simple form for updating the user's email address.
    Uses HTML5 validation + placeholders for accessibility.
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
    Form to allow users to change their username.
    Includes regex rules + length limits to prevent invalid names.
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
