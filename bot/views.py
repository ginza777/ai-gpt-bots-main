import json
from queue import Queue

from django.conf import settings
from django.http import JsonResponse
from telegram import Bot, Update
from telegram.ext import (
    CommandHandler,
    Dispatcher,
    MessageHandler, Filters,
    CallbackQueryHandler,
)

from bot.handlers import start, main_message_handler, handle_contact, handle_help_command, \
    handle_phone_number_contact

token = settings.AI_BOT_TOKEN

bot = settings.AI_BOT


def setup():
    queue = Queue()

    dp = Dispatcher(
        bot,
        queue,
        workers=12,
        use_context=True
    )
    dp = add_handlers(dp)

    return dp


def add_handlers(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", handle_help_command))
    dp.add_handler(CommandHandler("contact", handle_contact))
    dp.add_handler(MessageHandler(Filters.contact, handle_phone_number_contact))
    dp.add_handler(MessageHandler(Filters.text, main_message_handler))
    dp.add_handler(CallbackQueryHandler(main_inline_handler))
    return dp


def ai_bot_webhook(request, *args, **kwargs):
    update = Update.de_json(json.loads(request.body.decode("utf-8")), bot)
    dp = setup()
    dp.process_update(update)
    return JsonResponse({"status": "ok"})


def set_webhook(request):
    webhook_url = settings.DOMAIN + "/bot/webhook"
    bot = Bot(token=settings.AI_BOT_TOKEN)
    bot.set_webhook(url=webhook_url)
    return JsonResponse({"status": "ok"})
