from django.urls import path
from .views import ai_bot_webhook, set_webhook

urlpatterns = [
    path('webhook/', ai_bot_webhook),
    path('webhook', ai_bot_webhook),
    path('set/webhook/', set_webhook),
]
