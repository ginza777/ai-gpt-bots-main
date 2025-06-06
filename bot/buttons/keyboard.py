from telegram import KeyboardButton, ReplyKeyboardMarkup
from django.utils.translation import gettext_lazy as _
from ..translations import button_translate

#add  flag icon
languages = {
    "en": str(_("English 🇬🇧")),
    "uz": str(_("Uzbek 🇺🇿")),
    "ru": str(_("Russian 🇷🇺")),
}


def main_button_keyboard(lang='ru'):
    buttons = [
        [
            button_translate("about", lang=lang),
            button_translate("contact", lang=lang),
        ],
        [
            button_translate("settings", lang=lang),
            button_translate("github", lang=lang),
        ]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def language_button_keyboard():
    language_data = []
    res_data = []
    for language in languages.values():
        res_data.append(
            language
        )
        if len(res_data) == 2:
            language_data.append(res_data)
            res_data = []
    if res_data:
        language_data.append(res_data)
    return ReplyKeyboardMarkup(language_data, resize_keyboard=True)


def to_main_menu_keyboard(lang='ru'):
    buttons = [
        [
            button_translate("back_to_main_menu", lang=lang),
        ],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)



def settings_menu_keyboard(lang='ru'):
    buttons = [
        [
            button_translate("button_profile", lang=lang),
            button_translate("button_change_language", lang=lang),
        ],
        [
            button_translate("back_to_main_menu", lang=lang),
        ]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def phone_number_button_keyboard(lang='ru'):
    buttons = [
        [KeyboardButton(text=button_translate("button_share_phone_number", lang=lang), request_contact=True)]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
