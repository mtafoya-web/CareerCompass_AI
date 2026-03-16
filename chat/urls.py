from django.urls import path
from .views import chat_mentor_view, send_message, clear_chat

urlpatterns = [
    path("", chat_mentor_view, name="chat_mentor"),
    path("send/", send_message, name = "send_message"),
    path("clear/", clear_chat, name="clear_chat"),
]