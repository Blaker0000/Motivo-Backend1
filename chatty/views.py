# chatty/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from slack_sdk import WebClient
from django.conf import settings
from django.shortcuts import render
import json

@csrf_exempt
def slack_bot(request):
    """
    Handles Slack's event subscriptions.
    - Responds to the Slack 'challenge' parameter for URL verification.
    - Replies to messages posted in Slack (if you want to).
    """
    if request.method == "POST":
        data = json.loads(request.body)

        # If Slack is verifying the endpoint, it sends a 'challenge'
        if "challenge" in data:
            return JsonResponse({"challenge": data["challenge"]})

        # Slack event data
        event = data.get("event", {})
        text = event.get("text")       # The message text
        channel = event.get("channel") # The channel ID

        # Use your Slack Bot token from settings.py
        client = WebClient(token=settings.SLACK_BOT_TOKEN)

        # Example: echo the user’s text back to the channel
        if text and channel:
            client.chat_postMessage(channel=channel, text=f"You said: {text}")

        return JsonResponse({"status": "success"}, status=200)

    # If it’s not a POST request, return an error
    return JsonResponse({"error": "Invalid request"}, status=400)


def my_first_template_view(request):
    """
    Renders a simple HTML template located at:
    chatty/templates/chatty/my_template.html
    """
    return render(request, "chatty/my_template.html", {})
