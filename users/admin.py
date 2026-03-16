from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "campus",
        "major",
        "year",
        "target_roles",
        "available_hours_per_week",
    )
    search_fields = (
        "user__username",
        "user__email",
        "campus",
        "major",
        "year",
        "target_roles",
        "interests",
        "career_goals",
    )
    list_filter = ("campus", "year", "major")
    ordering = ("user__username",)
    list_per_page = 25

    fieldsets = (
        ("User Info", {
            "fields": ("user",)
        }),
        ("Academic Profile", {
            "fields": ("campus", "major", "year", "current_classes")
        }),
        ("Career Profile", {
            "fields": ("career_goals", "target_roles", "interests", "skills")
        }),
        ("Availability", {
            "fields": ("available_hours_per_week",)
        }),
    )