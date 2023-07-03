from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import exceptions
from account.authentication import UserTokenAuthentication


class AdminPermissions(BasePermission):
    def has_permission(self, request, view):

        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            try:
                user = request.user
            except:
                raise exceptions.AuthenticationFailed("No User Found")

            if user.is_superuser:
                return True
            else:
                return request.method in SAFE_METHODS
        else:
            return True
