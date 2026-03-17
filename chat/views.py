from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import ChatSession, ChatMessage
from .services.watson import chat_with_watson, WatsonAPIError
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

    student_context = {}
    if profile:
        student_context = {
            "student_profile": {
                "campus": profile.campus,
                "major": profile.major,
                "year": profile.year,
                "current_classes": profile.current_classes,
                "career_goals": profile.career_goals,
                "interests": profile.interests,
                "target_roles": profile.target_roles,
                "skills": profile.skills,
                "available_hours_per_week": profile.available_hours_per_week,
            }
        }

    try:
        assistant_reply = chat_with_watson(
            user_text=user_text,
            student_context=student_context,
        )
    except WatsonAPIError as exc:
        assistant_reply = f"I couldn't reach the Watson mentor service right now. {exc}"
    except Exception:
        assistant_reply = "I couldn't reach the Watson mentor service right now."

    ChatMessage.objects.create(
        session=session,
        sender="assistant",
        content=assistant_reply,
    )

    return JsonResponse({
        "assistant_message": assistant_reply,
    })


@login_required
@require_POST
def clear_chat(request):
    session = ChatSession.objects.filter(user=request.user).first()
    if session:
        ChatMessage.objects.filter(session=session).delete()
    return JsonResponse({"success": True})