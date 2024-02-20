from rest_framework import permissions
import sys


class ParkomateUserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            try:
                authorize = request.user.email == obj.email or request.user.privilege == 0 or request.user.is_superuser
                if authorize:
                    return True
                else:
                    False
            except AttributeError as e:
                _ = sys.exc_info()[0]
                return False
