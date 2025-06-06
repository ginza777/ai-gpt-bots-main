from django.contrib import admin
from .models import  Message




@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_user", "thread_id", "cost", "created_at", "updated_at", "response_message")
