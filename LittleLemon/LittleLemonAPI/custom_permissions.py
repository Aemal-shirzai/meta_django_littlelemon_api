from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied("You Need to be Manager to access this.")
        return True


def is_manager_check(request):
    return True if request.user.groups.filter(name='Manager').exists() else False

def is_crew_check(request):
    return True if request.user.groups.filter(name='Delivery Crew').exists() else False

def is_customer_check(request):
    return True if not is_manager_check(request) and not is_crew_check(request) else False