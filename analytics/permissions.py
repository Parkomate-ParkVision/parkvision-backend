from rest_framework import permissions
import sys


class AnalyticsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            authorize = request.user.is_superuser or request.user == request.user.organizations.owner
            if authorize:
                return True
            else:
                False
        except AttributeError as e:
            _ = sys.exc_info()[0]
            return False
