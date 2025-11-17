from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows login using either username or email.
    Django still handles password checking and permissions.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Allow login with 'username' field containing either username OR email
        user = None

        if username:
            # Try to match email first
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                # Fallback: try username
                try:
                    user = User.objects.get(username__iexact=username)
                except User.DoesNotExist:
                    return None

        # Validate password
        if user and user.check_password(password):
            return user

        return None
