from rest_framework import permissions

class isInstructor(permissions.BasePermission):
    def has_permission(self, request,view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Instructor').exists()
        return False