from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add this line to connect the chatty app's URLs:
    path("chatty/", include("chatty.urls")),
]
