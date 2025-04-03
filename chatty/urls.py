# chatty/urls.py

from django.urls import path
from .views import slack_bot, my_first_template_view

urlpatterns = [
    # Slack will POST events to this endpoint:
    path("slack-events/", slack_bot, name="slack_bot"),

    # A simple page to test an HTML template:
    path("hello-template/", my_first_template_view, name="my_template_view"),
]
