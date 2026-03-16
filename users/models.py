from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    YEAR_CHOICES = [
        ("freshman", "Freshman"),
        ("sophomore", "Sophomore"),
        ("junior", "Junior"),
        ("senior", "Senior"),
        ("graduate", "Graduate"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    campus = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES)
    current_classes = models.TextField(blank=True, help_text="Comma-separated classes")
    career_goals = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    target_roles = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True)
    available_hours_per_week = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.user.username} - {self.major}"
