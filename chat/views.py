from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import ChatSession, ChatMessage
from users.models import StudentProfile


@login_required
def chat_mentor_view(request):
    session, _ = ChatSession.objects.get_or_create(
        user=request.user,
        defaults={"title": "Main Chat"}
    )
    messages = session.messages.all().order_by("timestamp")
    return render(request, "chat/chat_mentor.html", {"messages": messages})


@login_required
@require_POST
def send_message(request):
    session, _ = ChatSession.objects.get_or_create(
        user=request.user,
        defaults={"title": "Main Chat"}
    )

    user_text = request.POST.get("message", "").strip()
    if not user_text:
        return JsonResponse({"error": "Message cannot be empty."}, status=400)

    ChatMessage.objects.create(
        session=session,
        sender="user",
        content=user_text,
    )

    profile = StudentProfile.objects.filter(user=request.user).first()
    assistant_reply = generate_mock_reply(profile, user_text)

    ChatMessage.objects.create(
        session=session,
        sender="assistant",
        content=assistant_reply,
    )

    return JsonResponse({
        "user_message": user_text,
        "assistant_message": assistant_reply,
    })


@login_required
@require_POST
def clear_chat(request):
    session = ChatSession.objects.filter(user=request.user).first()
    if session:
        ChatMessage.objects.filter(session=session).delete()
    return JsonResponse({"success": True})


def generate_mock_reply(profile, user_text):
    lowered = user_text.lower()

    if profile:
        major = profile.major
        year = profile.year
        role = profile.target_roles or "career growth"
    else:
        major = "student"
        year = "current"
        role = "career growth"

    if "internship" in lowered:
        return (
            f"As a {year} {major} student interested in {role}, "
            "your next best step is to strengthen one portfolio project "
            "and apply to a few roles this week."
        )

    if "project" in lowered:
        return (
            f"For a {major} student, a strong next project would be a practical app "
            "that shows real skills and can be discussed in interviews."
        )

    if "event" in lowered or "club" in lowered:
        return (
            "I’d focus on one relevant club and one event that matches your goals "
            "instead of trying to attend everything."
        )

    return (
        f"You’re a {year} {major} student. Based on your message, "
        "your next best action is to take one concrete career step this week."
    )