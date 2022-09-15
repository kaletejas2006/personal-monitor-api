"""
Tests for User API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL: str = reverse("user:create")
TOKEN_URL: str = reverse("user:token")
ME_URL: str = reverse("user:me")


def create_user(**kwargs):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**kwargs)


# Public features of an API are those that do not require authentication
# like registering a user.
class PublicUserAPITests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test for successful creation of a user."""
        payload: dict = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test User",
        }
        res: Response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Fetch information about an object in the database. Here, we
        # fetch the email address of the user created above.
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        # Check that the user specified password is not sent back as
        # part of the API response.
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test that error is returned if user with email already exists."""
        payload: dict = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test User",
        }
        # Create a user already so that our API call fails.
        create_user(**payload)
        res: Response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test that error is returned when the password is less than 5 characters."""
        payload: dict = {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test User",
        }
        res: Response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # When the password is too short, we do not create a new user and
        # this check is to ensure that.
        user_exists: bool = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test to check if token is created for valid credentials."""
        user_details: dict = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
        }
        create_user(**user_details)

        payload: dict = {
            "email": user_details["email"],
            "password": user_details["password"],
        }

        res: Response = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_incorrect_password(self):
        """Test to check that an error is thrown when password is invalid."""
        user_details: dict = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
        }
        create_user(**user_details)

        payload: dict = {
            "email": user_details["email"],
            "password": "untestpass123",
        }

        res: Response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_empty_password(self):
        """Test to check that an error is thrown when password is an empty string."""
        user_details: dict = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
        }
        create_user(**user_details)

        payload: dict = {
            "email": user_details["email"],
            "password": "",
        }

        res: Response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorised(self):
        """Test that authentication is required for users."""

        # Make an unauthorised request to the URL meant to manage a specific
        # user.
        res: Response = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        # Authenticate `APIClient()` with our test user before executing
        # every test.
        self.user = create_user(
            email="test@example.com", password="testpass123", name="Test User"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        # Basic test to ensure we can retrieve details of the test user
        # we forcefully logged in with.
        res: Response = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the ME endpoint"""
        # `POST` call should only be used to create objects (users here). To
        # modify existing objects, either of `PUT` or `PATCH` should be used.
        res: Response = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test user profile updates for authenticated users."""
        payload: dict = {"name": "New Test User", "password": "newtestpass123"}

        res: Response = self.client.patch(ME_URL, payload)

        # As the `patch` method does not return the user object, we need to
        # update it by directly fetching its details from the database.
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
