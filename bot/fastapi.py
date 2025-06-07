import os

import django

# Django sozlamalarini yuklash (agar Django ORM kerak bo‘lsa)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from queue import Queue

# Django settings import qilinadi
from django.conf import settings

# Sizning handlerlaringizni import qilasiz (pathni o‘zgartiring)
from bot.handlers import start, main_message_handler, handle_contact, handle_help_command, handle_phone_number_contact

app = FastAPI()

# Telegram bot token va bot obyektini olish
bot = Bot(token=settings.AI_BOT_TOKEN)


# Dispatcher yaratish va handlerlarni qo‘shish funksiyasi
def setup_dispatcher():
    queue = Queue()
    dp = Dispatcher(bot, queue, workers=4, use_context=True)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", handle_help_command))
    dp.add_handler(CommandHandler("contact", handle_contact))
    dp.add_handler(MessageHandler(Filters.contact, handle_phone_number_contact))
    dp.add_handler(MessageHandler(Filters.text, main_message_handler))
    return dp


dp = setup_dispatcher()

from fastapi.concurrency import run_in_threadpool


@app.post("/bot/webhook/")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await run_in_threadpool(dp.process_update, update)
    return {"status": "ok"}


@app.get("/set_webhook/")
async def set_webhook():
    webhook_url = settings.DOMAIN + "/bot/webhook"
    success = bot.set_webhook(url=webhook_url)
    return {"status": "webhook set" if success else "failed to set webhook"}
