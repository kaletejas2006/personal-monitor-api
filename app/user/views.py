"""
View for the user API.
"""
# The `rest_framework` package implements a lot of the logic required
# for adding objects to our database. Views are the ways in which
# our request to add/modify these objects are handled. These are provided
# by `rest_framework` in the form of base classes.
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import AuthTokenSerializer, UserSerializer


# `CreateAPIView` is designed to handle HTTP post requests for creating
# objects.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


# `ObtainAuthToken` is provided by Django for the creation of authorisation
# tokens. By default, it uses the username and password for generating the
# token but as we use email address instead of username, we override the
# default with our custom serializer.
class CreateTokenView(ObtainAuthToken):
    """Create a new authorisation token for user."""

    serializer_class = AuthTokenSerializer
    # `api_settings.DEFAULT_RENDERER_CLASSES` ensures that a nice, browsable
    # view of this API is rendered.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated object."""
        return self.request.user
