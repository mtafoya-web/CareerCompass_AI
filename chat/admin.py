from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    fields = ("sender", "content", "timestamp")
    readonly_fields = ("timestamp",)
    show_change_link = True


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "created_at", "message_count")
    search_fields = ("user__username", "title")
    ordering = ("-created_at",)
    list_per_page = 25
    readonly_fields = ("created_at",)
    inlines = [ChatMessageInline]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Messages"


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "sender", "short_content", "timestamp")
    search_fields = ("content", "session__user__username", "sender")
    list_filter = ("sender", "timestamp")
    ordering = ("-timestamp",)
    list_per_page = 50
    readonly_fields = ("timestamp",)

    def short_content(self, obj):
        return obj.content[:60] + "..." if len(obj.content) > 60 else obj.content
    short_content.short_description = "Content"