from rest_framework.permissions import BasePermission


class OwnerOrStuff(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return request.user.groups.filter(name='Moderators').exists()

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        elif request.method == 'DELETE':
            return False
        return request.user.groups.filter(name='Moderators').exists()
