from rest_framework import permissions


class IsAdminOrTeacher(permissions.BasePermission):
    """
    Permission class: Only admins and teachers
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'teacher']
        )


class IsAdminOrTeacherOrOwner(permissions.BasePermission):
    """
    Permission class: Admins, teachers, or the owner of the resource
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admins and teachers have full access
        if request.user.role in ['admin', 'teacher']:
            return True
        
        # Students can only access their own records
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsAdmin(permissions.BasePermission):
    """
    Permission class: Only admins
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )