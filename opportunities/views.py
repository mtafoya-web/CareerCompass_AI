from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from users.models import StudentProfile
from .models import Club, Event, InternshipOpportunity, ProjectIdea, MentorContact


def _split_csvish(text: str) -> list[str]:
    if not text:
        return []
    return [item.strip().lower() for item in text.split(",") if item.strip()]


def _matches_tags(obj_tags: str, desired_tags: list[str]) -> bool:
    if not desired_tags:
        return True
    source_tags = [tag.strip().lower() for tag in (obj_tags or "").split(",") if tag.strip()]
    return any(tag in source_tags for tag in desired_tags)


@login_required
def opportunities_dashboard(request):
    profile = StudentProfile.objects.filter(user=request.user).first()

    clubs = Club.objects.all()
    events = Event.objects.filter(date__gte=timezone.now()).order_by("date")
    internships = InternshipOpportunity.objects.all().order_by("deadline")
    projects = ProjectIdea.objects.all()
    mentors = MentorContact.objects.all()

    if profile:
        target_roles = _split_csvish(profile.target_roles)
        interests = _split_csvish(profile.interests)
        skills = _split_csvish(profile.skills)

        desired_tags = list(set(target_roles + interests + skills))

        clubs = [club for club in clubs if _matches_tags(club.tags, desired_tags)]
        events = [event for event in events if _matches_tags(event.tags, desired_tags)]
        internships = [
            internship
            for internship in internships
            if _matches_tags(internship.role_tags, desired_tags)
            or _matches_tags(internship.required_skills, desired_tags)
        ]
        projects = [
            project
            for project in projects
            if _matches_tags(project.role_tags, desired_tags)
            or _matches_tags(project.skill_tags, desired_tags)
        ]
        mentors = [mentor for mentor in mentors if _matches_tags(mentor.tags, desired_tags)]

    context = {
        "profile": profile,
        "clubs": clubs[:10],
        "events": events[:10],
        "internships": internships[:10],
        "projects": projects[:10],
        "mentors": mentors[:10],
    }
    return render(request, "opportunities/dashboard.html", context)