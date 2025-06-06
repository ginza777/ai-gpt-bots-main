import logging
from django.core.management.base import BaseCommand
from telegram.ext import Updater
from bot.views import add_handlers
from django.conf import settings

# Log sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def run_polling(token):
    """ Run bot in polling mode """
    updater = Updater(token, use_context=True)
    print(f"Bot token: {token}")

    # Dispatcher va handlerlarni sozlash
    dp = updater.dispatcher
    dp = add_handlers(dp)

    # Polling boshlash
    logger.info("Bot polling rejimida boshlandi.")
    updater.start_polling()
    updater.idle()


class Command(BaseCommand):
    help = "Run the Telegram bot in polling mode"

    def handle(self, *args, **kwargs):
        bot_token = settings.AI_BOT_TOKEN  # Faqat bitta bot tokeni
        run_polling(bot_token)