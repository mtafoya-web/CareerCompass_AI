from django.contrib import admin
from .models import Club, Event, InternshipOpportunity, ProjectIdea, MentorContact


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus', 'meeting_time')
    search_fields = ('name', 'campus', 'tags')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'campus', 'event_type', 'date')
    search_fields = ('title', 'campus', 'tags')
    list_filter = ('event_type', 'campus')


@admin.register(InternshipOpportunity)
class InternshipOpportunityAdmin(admin.ModelAdmin):
    list_display = ('company', 'title', 'location', 'deadline')
    search_fields = ('company', 'title', 'role_tags')


@admin.register(ProjectIdea)
class ProjectIdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty')
    search_fields = ('title', 'skill_tags', 'role_tags')


@admin.register(MentorContact)
class MentorContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'company')
    search_fields = ('name', 'role', 'company', 'tags')