from django.urls import path
from .views import recommendations_dashboard

urlpatterns = [
    path("", recommendations_dashboard, name="recommendations_dashboard"),
]