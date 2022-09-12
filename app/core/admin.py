"""Django admin customisation."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Future-proofing for translation requirements in the future. When the
# default language of our application is changed, fieldsets with `_`
# are automatically translated.
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering: list = ["id"]
    list_display: list = ["email", "name"]

    fieldsets: tuple = (
        # The fieldsets can be dynamically updated without needing to
        # recreate the containers.
        # We set the fieldset title to `None`.
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        # The code fails without the comma after "last_login" as fields input
        # should either be a tuple or list.
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields: list = ["last_login"]

    add_fieldsets: tuple = (
        (
            None,
            {
                # `wide` is a Django-specific CSS class that makes the layout
                # of the "Add User" page neater.
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


# Register both the user model and how the admin page should be structured.
admin.site.register(models.User, UserAdmin)
