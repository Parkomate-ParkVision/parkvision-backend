from rest_framework import permissions
import sys


class ParkingPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            try:
                authorize = request.user.is_superuser or request.user == obj.organization.owner
                if authorize:
                    return True
                else:
                    False
            except AttributeError as e:
                _ = sys.exc_info()[0]
                return False


class CCTVPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            try:
                authorize = request.user.is_superuser or request.user == obj.parking.organization.owner
                if authorize:
                    return True
                else:
                    False
            except AttributeError as e:
                _ = sys.exc_info()[0]
                return False
