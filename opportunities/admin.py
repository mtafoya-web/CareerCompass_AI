from django.contrib import admin
from .models import  Club, MentorContact, Events, InternshipOpportunity, ProjectIdea
# Register your models here.
admin.site.register(Club, MentorContact, Events, InternshipOpportunity, ProjectIdea)