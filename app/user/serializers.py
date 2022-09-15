"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

# The `rest_framework` contains various tools for serializers which are
# ways to convert to and from Python objects. For example, a JSON input
# from an API call is accepted and validated by a serializer based on
# the rules specified and then the requested Python object or a model
# in our database is returned.
from rest_framework import serializers


# `ModelSerializer` allows us to automatically validate and save things
# in a model based on the serializer rules.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # Class to inform `ModelSerializer` about the model to use, the fields
    # our entry should contain, and the rules to apply. Here, we only
    # specify the fields that can be changed by the user through the API
    # and thus admin fields like `is_superuser` are not mentioned.
    class Meta:
        model = get_user_model()
        fields: list = ["email", "password", "name"]
        # `write_only` ensures that the password value is only written
        # to the database and not returned with the response. These arguments
        # must be provided as a dictionary named `extra_kwargs`.
        extra_kwargs: dict = {"password": {"write_only": True, "min_length": 5}}

    # By default, the serializer will create a default object according
    # to our model. But as we are dealing with passwords here that should
    # not be visible, we override the default `create` method so that it
    # is only executed when the data has been already validated by the
    # serializer.
    def create(self, validated_data: dict):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    # `instance` here is the model instance to be updated.
    def update(self, instance, validated_data: dict):
        """Update and return user."""
        password: str = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication token."""

    # We initialise the serializer with the email and password fields.
    email: serializers.EmailField = serializers.EmailField()
    # Although the password will mostly be provided in some code, during
    # testing, we want the password text box to not show the actual password
    # hence we add the relevant style. Also, Django trims leading and
    # trailing whitespaces from strings but passwords might legitimately
    # contain whitespaces so, we turn the trimming off.
    password: serializers.CharField = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs: dict) -> dict:
        """Validate and authenticate the user."""
        email: str = attrs.get("email")
        password: str = attrs.get("password")
        # `authenticate` is a function provided by Django to authenticate
        # the input credentials. The `request` attribute accepts request
        # metadata like headers. If authentication is successful, the user
        # object is returned. If not, `None` is returned.
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg: str = _("Unable to authenticate with input credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
