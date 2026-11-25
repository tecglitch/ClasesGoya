from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import nh3

from rest_framework import serializers

from .models import Project, Tag, Task
from .services import HolidayService

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    due_on_holiday = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "project", "title", "description", "priority",
            "status", "due_date", "tags", "due_on_holiday", "created_at",
        ]

    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("La fecha límite no puede estar en el pasado.")
        return value

    def validate_description(self, value):
        return nh3.clean(value, tags=set())

    def validate(self, data):
        status = data.get("status", getattr(self.instance, "status", None))
        due_date = data.get("due_date", getattr(self.instance, "due_date", None))
        if status == "completada" and not due_date:
            raise serializers.ValidationError(
                "No se puede marcar una tarea como completada sin fecha límite registrada."
            )

        project = data.get("project", getattr(self.instance, "project", None))
        if status == "en_progreso" and project:
            completed = Task.objects.filter(project=project, status="completada")
            if self.instance:
                completed = completed.exclude(pk=self.instance.pk)
            if not completed.exists():
                raise serializers.ValidationError(
                    "El proyecto debe tener una tarea completada antes de iniciar otra."
                )
        return data

    def get_due_on_holiday(self, task):
        return bool(task.due_date and HolidayService.is_holiday(task.due_date))


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "tasks", "created_at"]
