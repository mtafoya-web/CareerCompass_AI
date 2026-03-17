from django.urls import path
from .views import opportunities_dashboard

urlpatterns = [
    path("", opportunities_dashboard, name="opportunities_dashboard"),
]