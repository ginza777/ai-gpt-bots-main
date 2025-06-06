from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def plans_inline_button(plans):
    res_data = []
    data = []
    for plan in plans:
        res_data.append(
            InlineKeyboardButton(
                text=plan.title,
                callback_data=f"plan_{plan.id}",
            )
        )
        if len(res_data) == 2:
            data.append(res_data)
            res_data = []
    if len(res_data) > 0:
        data.append(res_data)
    return InlineKeyboardMarkup(data)
