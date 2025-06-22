from rest_framework import permissions
from django.contrib.auth.models import Group

class IsAdmin(permissions.BasePermission):
    """
    Permite acesso apenas a usuários no grupo 'Administrador'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Administrador').exists()

class IsFinanceiro(permissions.BasePermission):
    """
    Permite acesso total apenas para membros do grupo 'Financeiro'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
            request.user.groups.filter(name="Financeiro").exists()

class IsProfessor(permissions.BasePermission):
    """
    Permite acesso apenas para membros do grupo 'Professor'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
            request.user.groups.filter(name="Professor").exists()

class IsGestor(permissions.BasePermission):
    """
    Permite acesso apenas para membros do grupo 'Gestor'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
            request.user.groups.filter(name="Gestor").exists()

