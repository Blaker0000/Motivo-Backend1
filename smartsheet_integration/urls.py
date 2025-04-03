from django.urls import path
from .views import fetch_workspaces, workspace_detail

urlpatterns = [
    path('workspaces/', fetch_workspaces, name='fetch_workspaces'),
    path('workspaces/<int:workspace_id>/', workspace_detail, name='workspace_detail'),
]
