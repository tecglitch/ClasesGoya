from .models import Task


class TaskRepository:
    @staticmethod
    def get_queryset():
        return (
            Task.objects.select_related("project")
            .prefetch_related("tags")
            .order_by("-created_at", "-id")
        )
