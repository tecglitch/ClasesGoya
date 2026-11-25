import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Project, ProjectMembership, SecurityLog, Task
from .permissions import IsProjectAdminOrReadOnly
from .repositories import TaskRepository
from .serializers import ProjectSerializer, TaskSerializer, UserRegistrationSerializer
from .services import MembershipService, NotificationService, ProjectService, TaskService
from .throttles import LoginRateThrottle

security_logger = logging.getLogger("security")


def health_check(request):
    return JsonResponse({"status": "ok", "service": "TaskFlow API"})


def api_version(request):
    return JsonResponse({"version": "0.1.0"})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related("tasks__tags").order_by("id")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAdminOrReadOnly]

    def get_queryset(self):
        return MembershipService.projects_for(self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            project = serializer.save()
            ProjectMembership.objects.create(
                project=project, user=self.request.user, role="admin"
            )

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        project = self.get_object()
        return Response(ProjectService.project_summary(project))

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):
        project = self.get_object()
        username = request.data.get("username", "").strip()
        role = request.data.get("role", "miembro")
        if role not in dict(ProjectMembership.ROLE_CHOICES):
            return Response({"detail": "Rol inválido."}, status=status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.filter(username=username).first()
        if user is None:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        try:
            with transaction.atomic():
                membership, created = ProjectMembership.objects.get_or_create(
                    project=project, user=user, defaults={"role": role}
                )
        except IntegrityError:
            created = False
        if not created:
            return Response({"detail": "El usuario ya es miembro del proyecto."}, status=400)
        return Response(
            {"username": username, "role": membership.role},
            status=status.HTTP_201_CREATED,
        )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskRepository.get_queryset()
    serializer_class = TaskSerializer
    filterset_fields = ["status", "priority", "project"]
    ordering_fields = ["due_date", "created_at", "priority"]
    search_fields = ["title", "description"]
    permission_classes = [IsAuthenticated, IsProjectAdminOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(
            project__memberships__user=self.request.user
        ).distinct()

    def check_project_admin(self, project):
        if not MembershipService.is_admin(self.request.user, project):
            SecurityLog.objects.create(
                user=self.request.user,
                action="permission_denied",
                detail=f"method={self.request.method} project={project.pk}",
                ip_address=self.request.META.get("REMOTE_ADDR"),
            )
            raise PermissionDenied("Solo un admin del proyecto puede crear o mover tareas en él.")

    def perform_create(self, serializer):
        self.check_project_admin(serializer.validated_data["project"])
        task = serializer.save(owner=self.request.user)
        NotificationService.notify_task_created(task)

    def perform_update(self, serializer):
        if "project" in serializer.validated_data:
            self.check_project_admin(serializer.validated_data["project"])
        task = serializer.save()
        NotificationService.notify_task_updated(task)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task = TaskService.mark_completed(task)
        NotificationService.notify_task_completed(task)
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def overdue(self, request):
        tasks = TaskService.tasks_overdue(self.get_queryset())
        page = self.paginate_queryset(tasks)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(tasks, many=True).data)


class RegisterView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class SocialLoginJWTView(APIView):
    def get(self, request):
        refresh = RefreshToken.for_user(request.user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            ip_address = request.META.get("REMOTE_ADDR")
            username = str(request.data.get("username", ""))[:150].replace("\n", "")
            SecurityLog.objects.create(
                action="login_failed",
                detail=f"usuario={username}",
                ip_address=ip_address,
            )
            security_logger.warning(
                "Login fallido para usuario %s desde %s", username, ip_address
            )
            raise
