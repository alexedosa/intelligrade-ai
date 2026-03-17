from rest_framework.permissions import BasePermission

class isAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'

class isLecturer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Lecturer'
    

class isStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Student'