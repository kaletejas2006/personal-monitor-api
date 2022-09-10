"""Database models."""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **kwargs):
        """Create, save, and return a new user."""
        if not email:
            raise ValueError("User must have a valid email address.")
        # `**kwargs` includes additional fields like username, is_active, etc.
        user: User = self.model(email=self.normalize_email(email), **kwargs)
        # `set_password()` converts a human-readable password to a string
        # of random characters using a one-way hash. It is set to optional
        # in order to create users for testing that do not need access.
        user.set_password(password)
        # With the `using` argument, the user can be saved in multiple
        # databases at once if required.
        # TODO: What is `self._db`?
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and return a new superuser.

        A user with `is_staff` set to True has access to Django admin.
        A superuser, provided that `is_staff` is `True`, has all permissions
        in Django admin.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# `AbstractBaseUser` contains all the functionality for authentication.
# `PermissionsMixin` contains all the functionality for permissions and fields.
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=False)
    is_active = models.BooleanField(default=True)
    # `is_staff` determines whether a user can log into Django admin.
    is_staff = models.BooleanField(default=False)

    # Assign user manager to our user class.
    # TODO: What does this mean?
    objects = UserManager()

    USERNAME_FIELD = "email"
