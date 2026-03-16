from django.urls import path
from .views import chat_mentor_view

urlpatterns = [
    path("chat/", chat_mentor_view, name="chat_mentor"),
]