from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q

from users.models import StudentProfile
from opportunities.models import (
    Club,
    Event,
    InternshipOpportunity,
    ProjectIdea,
    MentorContact,
)
from .models import Recommendation


def _split_csvish(text: str) -> list[str]:
    if not text:
        return []
    return [item.strip().lower() for item in text.split(",") if item.strip()]


def _score_text(text: str, keywords: list[str]) -> int:
    if not text:
        return 0
    text = text.lower()
    return sum(1 for word in keywords if word and word in text)


@login_required
def recommendations_dashboard(request):
    profile = StudentProfile.objects.filter(user=request.user).first()

    if not profile:
        return render(
            request,
            "recommendations/dashboard.html",
            {
                "profile_missing": True,
                "recommendations": [],
            },
        )

    keywords = list(
        set(
            _split_csvish(profile.major)
            + _split_csvish(profile.interests)
            + _split_csvish(profile.skills)
            + _split_csvish(profile.target_roles)
            + _split_csvish(profile.current_classes)
        )
    )

    generated = []

    for club in Club.objects.all():
        score = _score_text(club.tags, keywords) + _score_text(club.description, keywords)
        if score > 0:
            generated.append({
                "type": "club",
                "title": club.name,
                "description": club.description,
                "reason": f"Matches your interests/skills through tags: {club.tags}",
                "priority_score": float(score),
            })

    for event in Event.objects.all():
        score = _score_text(event.tags, keywords) + _score_text(event.description, keywords)
        if score > 0:
            generated.append({
                "type": "event",
                "title": event.title,
                "description": event.description,
                "reason": f"Relevant event based on your profile tags: {event.tags}",
                "priority_score": float(score),
            })

    for internship in InternshipOpportunity.objects.all():
        score = (
            _score_text(internship.role_tags, keywords)
            + _score_text(internship.required_skills, keywords)
            + _score_text(internship.description, keywords)
        )
        if score > 0:
            generated.append({
                "type": "internship",
                "title": f"{internship.company} - {internship.title}",
                "description": internship.description,
                "reason": "This internship lines up with your target roles and skill set.",
                "priority_score": float(score),
            })

    for project in ProjectIdea.objects.all():
        score = (
            _score_text(project.role_tags, keywords)
            + _score_text(project.skill_tags, keywords)
            + _score_text(project.description, keywords)
        )
        if score > 0:
            generated.append({
                "type": "project",
                "title": project.title,
                "description": project.description,
                "reason": "This project can help build experience in your target area.",
                "priority_score": float(score),
            })

    for mentor in MentorContact.objects.all():
        score = _score_text(mentor.tags, keywords) + _score_text(mentor.bio, keywords)
        if score > 0:
            generated.append({
                "type": "mentor",
                "title": f"{mentor.name} - {mentor.role}",
                "description": mentor.bio,
                "reason": "This mentor appears relevant to your academic and career interests.",
                "priority_score": float(score),
            })

    generated.sort(key=lambda x: x["priority_score"], reverse=True)
    top_recommendations = generated[:10]

    # Optional: store/update in DB each time the page is loaded
    Recommendation.objects.filter(user=request.user, is_completed=False).delete()

    saved_recommendations = []
    for item in top_recommendations:
        rec = Recommendation.objects.create(
            user=request.user,
            recommendation_type=item["type"],
            title=item["title"],
            description=item["description"],
            reason=item["reason"],
            priority_score=item["priority_score"],
        )
        saved_recommendations.append(rec)

    return render(
        request,
        "recommendations/dashboard.html",
        {
            "profile_missing": False,
            "recommendations": saved_recommendations,
            "profile": profile,
        },
    )