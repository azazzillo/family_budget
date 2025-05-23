# Rest
from rest_framework.permissions import BasePermission
# Local
from .models import FamilyUser, Family


class IsFamilyMember(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user

        return (
                Family.objects.filter(owner=user).exists() or
                FamilyUser.objects.filter(member=user).exists()
            )