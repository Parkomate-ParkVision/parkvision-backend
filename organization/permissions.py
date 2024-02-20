from rest_framework import permissions
import sys


class OrganizationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            try:
                authorize = request.user.is_superuser or request.user == obj.owner or request.user.privilege == 0
                if authorize:
                    return True
                else:
                    return False
            except AttributeError as e:
                _ = sys.exc_info()[0]
                return False
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            try:
                authorize = request.user.is_superuser or request.user == obj.owner or request.user.privilege == 0
                if authorize:
                    return True
                else:
                    return False
            except AttributeError as e:
                _ = sys.exc_info()[0]
                return False


class GatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            try:
                authorize = request.user.is_superuser or request.user == obj.organization.owner or request.user.privilage == 0
                if authorize:
                    return True
                else:
                    return False
            except AttributeError as e:
                _ = sys.exc_info()[0]
                return False


class DashboardPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            authorize = request.user.is_superuser or request.user == obj.organization.owner or request.user.privilage == 0
            if authorize:
                return True
            else:
                return False
        except AttributeError as e:
            _ = sys.exc_info()[0]
            return False
