from rest_framework.permissions import BasePermission
from rest_framework import permissions


class DeleteAdminOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["POST", "PUT", "PATCH"]:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return request.user.is_staff
