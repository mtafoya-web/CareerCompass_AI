from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    path("", include("users.urls")),
    path("opportunities/", include("opportunities.urls")),
    path("recommendations/", include("recommendations.urls")),
]