from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "due_date",
        "importance",
        "estimated_hours",
        "created_at",
    )
    list_filter = ("importance", "due_date")
    search_fields = ("title",)
