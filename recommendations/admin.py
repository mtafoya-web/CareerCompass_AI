from django.contrib import admin
from .models import Recommendation, ActionPlanItem


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recommendation_type",
        "title",
        "priority_score",
        "is_completed",
        "created_at",
    )
    search_fields = (
        "user__username",
        "title",
        "description",
        "reason",
        "recommendation_type",
    )
    list_filter = ("recommendation_type", "is_completed", "created_at")
    ordering = ("-priority_score", "-created_at")
    list_per_page = 25
    readonly_fields = ("created_at",)

    fieldsets = (
        ("User", {
            "fields": ("user",)
        }),
        ("Recommendation", {
            "fields": ("recommendation_type", "title", "description", "reason")
        }),
        ("Status", {
            "fields": ("priority_score", "is_completed", "created_at")
        }),
    )


@admin.register(ActionPlanItem)
class ActionPlanItemAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "status", "due_date", "created_at")
    search_fields = ("user__username", "title", "description", "status")
    list_filter = ("status", "due_date", "created_at")
    ordering = ("status", "due_date")
    list_per_page = 25
    readonly_fields = ("created_at",)

    fieldsets = (
        ("User", {
            "fields": ("user",)
        }),
        ("Task", {
            "fields": ("title", "description")
        }),
        ("Timeline", {
            "fields": ("due_date", "status", "created_at")
        }),
    )