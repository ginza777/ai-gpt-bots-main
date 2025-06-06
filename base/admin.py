from django.contrib import admin
from .models import TelegramUser, TelegramBotUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', "full_name", "balance", "created_at", "updated_at")
    list_filter = ("language",)


@admin.register(TelegramBotUser)
class TelegramBotUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_user", "bot", "created_at", "updated_at")
    list_filter = ("bot",)
