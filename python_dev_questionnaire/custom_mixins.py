from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class OwnershipRequiredMixin(PermissionRequiredMixin):
    """
    Checks if the user is authenticated and has appropriate permissions.
    For users: allows managing only their own profiles.

    Valid ownership_field values:
        - 'user' for users
    """
    ownership_field = None
    permission_denied_redirect_url = None
    permission_denied_message = None

    _owner_mapping = {
        'user': lambda x: x.id,
    }

    def get_owner(self):
        """
        Returns the owner of the model object based on the ownership_field.
        """
        obj = self.get_object()
        return self._owner_mapping[self.ownership_field](obj)

    def has_permission(self):
        """
        Overriding has_permission method from PermissionRequiredMixin.
        Checks if the user has permission to manage the object.
        """
        return self.get_owner() == self.request.user.id

    def handle_no_permission(self):
        """
        Overriding handle_no_permission method from AccessMixin.
        If the user is not authenticated, redirects to the login page.
        If the user has no permission, redirects to the specified index page.
        """
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Пожалуйста, войдите в систему, чтобы выполнить это действие',
            )
            return super().handle_no_permission()

        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse_lazy(self.permission_denied_redirect_url))
