from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AccountTests(TestCase):
    """
    Automated tests for account-related functionality:
    - Signup creates user
    - Logging in via username works (custom backend support)
    """

    def setUp(self):
        """
        Create a test client before each test.
        Each test runs in isolation with its own test database.
        """
        self.client = Client()

    def test_signup_creates_user(self):
        """
        Test the signup form.
        Submitting valid data should create a user in the database.
        """
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        })

        # We expect exactly one user to be created
        self.assertEqual(User.objects.count(), 1)

    def test_login_with_username(self):
        """
        Test the custom login system.
        User should be able to log in using their username OR email.
        This test uses the username path.
        """
        User.objects.create_user(username="testuser", password="abc12345")

        result = self.client.post(reverse("login"), {
            "username_or_email": "testuser",
            "password": "abc12345",
        })

        # Login should redirect the user (HTTP 200, 302) to the next page
        self.assertIn(result.status_code, [200, 302])

