from datetime import datetime

from django.conf import settings
from telegram import LabeledPrice
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext

from base.models import TelegramUser
from bot.translations import translate, button_translate
from .buttons.inline import plans_inline_button
from .buttons.keyboard import main_button_keyboard, language_button_keyboard, languages, to_main_menu_keyboard,settings_menu_keyboard, phone_number_button_keyboard
from .models import  Message
from .tasks import check_message_result_with_message_id
#import parse mode
from telegram import ParseMode
client = settings.OPENAI_CLIENT

TEXT_PROMPTS = {
    "ru": "Вы — умный AI-помощник",
    "uz": "Siz aqlli AI yordamchisiz.",
    "en": "You are a smart AI assistant"
}


def get_user_lang(telegram_id):
    tg_user = TelegramUser.objects.get(telegram_id=telegram_id)
    return tg_user.language or 'uz'


def start(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.filter(
        telegram_id=update.effective_user.id if hasattr(update, "effective_user") else update.from_user.id).first()
    if not user or not user.language:
        update.message.reply_text(
            translate("ask_language"),
            reply_markup=language_button_keyboard(),
        )
        TelegramUser.objects.create(
            telegram_id=update.effective_user.id,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
            username=update.effective_user.username
        )
        return

    if not user.full_name:
        update.message.reply_text(translate("ask_full_name", user.language), reply_markup=ReplyKeyboardRemove())
        return
    if not user.phone_number:
        update.message.reply_text(translate("ask_phone_number", user.language),
                                  reply_markup=phone_number_button_keyboard())
        return
    update.message.reply_text(
        translate("start", user.language),
        reply_markup=main_button_keyboard(user.language),
    )


def handle_full_name(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.get(telegram_id=update.effective_user.id)
    full_name = update.message.text
    user.full_name = full_name
    user.save(
        update_fields=["full_name"]
    )
    update.message.reply_text(
        translate("ask_phone_number", user.language),
        reply_markup=phone_number_button_keyboard()
    )


def handle_language(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.get(telegram_id=update.effective_user.id)
    language = update.message.text.strip()
    if language not in languages.values():
        start(update, context)
        return
    for lang_code, lang_text in languages.items():
        if lang_text == language:
            user.language = lang_code
            user.save(
                update_fields=["language"]
            )
            break
    return start(update, context)


def is_valid_uz_phone(number: str) -> bool:
    number.replace(' ', '')
    if number[0] == "+":
        number = number[1:]
    if not number.isdigit():
        return False
    return True


def handle_phone_number(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.filter(telegram_id=update.effective_user.id).first()
    phone_number = update.message.text
    if not is_valid_uz_phone(phone_number):
        update.message.reply_text(
            translate("ask_phone_number", user.language),
            reply_markup=phone_number_button_keyboard()
        )
        return
    user.phone_number = phone_number
    user.save(
        update_fields=["phone_number"]
    )
    return main_menu(update, context)


def handle_phone_number_contact(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.filter(telegram_id=update.effective_user.id).first()
    phone_number = update.message.contact.phone_number
    user.phone_number = phone_number
    user.save(
        update_fields=["phone_number"]
    )
    return main_menu(update, context)


def main_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        translate("main_menu", get_user_lang(update.effective_user.id)),
        reply_markup=main_button_keyboard(lang=get_user_lang(update.effective_user.id)),
    )


def handle_about_section(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        translate("about_section", get_user_lang(update.effective_user.id)),
        reply_markup=main_button_keyboard(get_user_lang(update.effective_user.id)),
    )


def handle_github_section(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        translate("github_section", get_user_lang(update.effective_user.id)),
        reply_markup=main_button_keyboard(get_user_lang(update.effective_user.id)),
        parse_mode=ParseMode.HTML
    )


def handle_contact(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        translate("contact", get_user_lang(update.effective_user.id)),
        reply_markup=main_button_keyboard(get_user_lang(update.effective_user.id)),
    )


def handle_help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        translate("help", get_user_lang(update.effective_user.id)),
        reply_markup=main_button_keyboard(get_user_lang(update.effective_user.id)),
    )



def handle_settings(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.filter(telegram_id=update.effective_user.id).first()
    update.message.reply_text(
        translate("settings_main_message", user.language), reply_markup=settings_menu_keyboard(user.language),
    )


def handle_change_language(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        translate("ask_language"),
        reply_markup=language_button_keyboard()
    )


def handle_profile(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.get(telegram_id=update.effective_user.id)
    used_days = (datetime.today().date() - user.created_at.date()).days
    update.message.reply_text(
        translate("profile_message", get_user_lang(update.effective_user.id),
                  telegram_id=user.telegram_id,
                  fullname=f"{user.first_name} {user.last_name}",
                  phone_number=user.phone_number,
                  language=user.language,
                  balance=user.balance,
                  used_days=used_days
                  ),
        reply_markup=settings_menu_keyboard(user.language),
    )


def gpt_handle_text(update: Update, context: CallbackContext):
    message = update.message
    if not message:
        return

    uid = message.from_user.id
    user = TelegramUser.objects.get(telegram_id=uid)
    text = message.text
    lang = user.language

    instruction = {
        "ru": "Отвечай на русском языке.",
        "uz": "O'zbek tilida javob ber.",
        "en": "Answer in English."
    }.get(lang, "Answer in English.")
    thread_id = user.get_thread_id(settings.AI_BOT.username)
    print("thread_id", thread_id)
    telegram_message = message.reply_text(translate("waiting_response_message", user.language))
    response = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=f"{TEXT_PROMPTS[lang]}\n{instruction}\n\n{text}"
    )
    print(response, "response")
    run = client.beta.threads.runs.create(thread_id=thread_id,
                                          assistant_id=settings.ASSISTANT_ID)
    print(run, "run")
    is_finished = False
    is_on_process = True
    response_message = None
    if run.status == "completed":
        response = client.beta.threads.messages.list(thread_id=thread_id, order="desc").data[0].content[
            0].text.value
        context.bot.edit_message_text(
            text=response,
            chat_id=user.telegram_id,
            message_id=telegram_message.message_id
        )
        response_message = response
        is_finished = True
    message = Message.objects.create(
        telegram_user=user,
        thread_id=thread_id,
        input_message=text,
        run_id=run.id,
        telegram_message_id=telegram_message.message_id,
        is_finished=is_finished,
        is_on_process=is_on_process,
        response_message=response_message
    )
    if not message.is_finished:
        check_message_result_with_message_id.apply_async(countdown=2, args=[message.id])


def main_message_handler(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.objects.filter(telegram_id=update.effective_user.id).first()
    message = update.message.text.strip()
    if not user:
        return start(update, context)
    if not user.language or message in list(languages.values()):
        return handle_language(update, context)
    if not user.full_name:
        return handle_full_name(update, context)
    if button_translate("about", user.language).strip() == message:
        return handle_about_section(update, context)
    if button_translate("github", user.language).strip() == message:
        return handle_github_section(update, context)
    if button_translate("contact", user.language).strip() == message:
        return handle_contact(update, context)
    if button_translate("settings", user.language).strip() == message:
        return handle_settings(update, context)
    if button_translate("button_change_language", user.language).strip() == message:
        return handle_change_language(update, context)
    if button_translate("button_profile", user.language).strip() == message:
        return handle_profile(update, context)
    if button_translate("back_to_main_menu", user.language).strip() == message:
        return start(update, context)
    return gpt_handle_text(update, context)

