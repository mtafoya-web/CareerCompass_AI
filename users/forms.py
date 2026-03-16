from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            "campus",
            "major",
            "year",
            "current_classes",
            "career_goals",
            "interests",
            "target_roles",
            "skills",
            "available_hours_per_week",
        ]
        widgets = {
            "career_goals": forms.Textarea(attrs={"rows": 4}),
            "current_classes": forms.Textarea(attrs={"rows": 3}),
            "interests": forms.Textarea(attrs={"rows": 3}),
            "skills": forms.Textarea(attrs={"rows": 3}),
        }