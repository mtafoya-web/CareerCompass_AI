from django.db import models

class Club(models.Model):
    name = models.CharField(max_length = 150)
    campus = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    tags = models.CharField(max_length = 255, blank = True)
    meeting_time = models.CharField(max_length=255, blank = True)
    link = models.URLField(blank = True)

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPES = [
        ("career_fair", "Career Fair"),
        ("workshop", "Workshop"),
        ("hackathon", "Hackathon"),
        ("networking", "Networking"),
        ("club_event", "Club Event"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    campus = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default="other")
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

class InternshipOpportunity(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    required_skills = models.TextField(blank=True)
    role_tags = models.CharField(max_length=255, blank=True)
    application_link = models.URLField(blank=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.title}"

class ProjectIdea(models.Model):
    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    skill_tags = models.CharField(max_length=255, blank=True)
    role_tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class MentorContact(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    major = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
