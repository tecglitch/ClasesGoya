from rest_framework import permissions

from .models import SecurityLog
from .services import MembershipService


class IsProjectAdminOrReadOnly(permissions.BasePermission):
    """Miembros leen; solo admins del proyecto pueden modificar."""

    def has_object_permission(self, request, view, obj):
        project = obj.project if hasattr(obj, "project") else obj
        if request.method in permissions.SAFE_METHODS:
            return MembershipService.is_member(request.user, project)
        allowed = MembershipService.is_admin(request.user, project)
        if not allowed:
            SecurityLog.objects.create(
                user=request.user,
                action="permission_denied",
                detail=f"method={request.method} project={project.pk}",
                ip_address=request.META.get("REMOTE_ADDR"),
            )
        return allowed
