"""
Tests for models
"""

# Base test class provided by Django.
from django.test import TestCase

# `get_user_model` is a helper function to retrieve the default user model
# of a project. When defining a custom model, we need to explicitly configure
# `get_user_model` to retrieve it by default.
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        # `example.com` is a reserved domain address meant for testing.
        # Hence, its use is highly recommended especially during tests on
        # sending emails to prevent sending them to real users accidentally.
        email: str = "test@example.com"
        password: str = "pass123"
        # `objects` is a reference to the model manager that we create.
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        # Passwords are saved as one-way hash by default. Hence, Django
        # provides a helper function to check password by its hash value.
        self.assertTrue(user.check_password(password))

    def test_new_user_email_is_normalised(self):
        """Test a new user email is normalised."""
        sample_emails: list = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@EXAMPLE.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        email: str
        expected: str
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_user_raises_error(self):
        """Test that creating a user without an email raises a `ValueError`."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser("test@example.com", "test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
