from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied("You Need to be Manager to access this.")
        return True

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name='Delivery crew').exists():
            raise PermissionDenied("You Need to be Delivery crew to access this.")
        return True