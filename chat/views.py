from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ChatSession, ChatMessage
from users.models import StudentProfile


@login_required
def chat_mentor_view(request):
    session, _ = ChatSession.objects.get_or_create(user=request.user, title="Main Chat")

    if request.method == "POST":
        user_text = request.POST.get("message", "").strip()

        if user_text:
            ChatMessage.objects.create(
                session=session,
                sender="user",
                content=user_text
            )

            profile = StudentProfile.objects.get(user=request.user)

            assistant_reply = generate_mock_reply(profile, user_text)

            ChatMessage.objects.create(
                session=session,
                sender="assistant",
                content=assistant_reply
            )

        return redirect("chat_mentor")

    messages = session.messages.all().order_by("timestamp")
    return render(request, "chat/chat.html", {"messages": messages})


def generate_mock_reply(profile, user_text):
    return (
        f"You are a {profile.year} {profile.major} student. "
        f"Based on your goal, your next best step is to build one project this week "
        f"and attend one relevant campus event."
    )