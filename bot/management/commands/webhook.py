import requests
from django.conf import settings
from django.core.management.base import BaseCommand

token = settings.AI_BOT_TOKEN  # Faqat bitta bot tokenini olish


def set_webhook():
    bot_token = settings.AI_BOT_TOKEN
    webhook_url = settings.DOMAIN
    url_webhook = f"{webhook_url}/bot/webhook/"
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={url_webhook}"
    return requests.post(url)


def get_webhook(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    return requests.post(url).json()


class Command(BaseCommand):
    help = "Set webhook for a single bot"

    def handle(self, *args, **options):
        # Webhookni sozlash
        set_webhook_response = set_webhook()
        # Webhook ma'lumotlarini olish
        webhook_info = get_webhook(token)

        username = requests.post(f"https://api.telegram.org/bot{token}/getMe").json().get("result").get("username")

        print("\n\n", 100 * "-")
        print(f"Webhook set for bot: https://t.me/{username}")
        print(f"Webhook URL: {webhook_info.get('result').get('url')}")
        print(f"Set Webhook Status: {set_webhook_response.status_code}")
        print("Webhook set and info fetched successfully for the bot\n\n")
