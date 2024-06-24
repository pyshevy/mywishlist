from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def conf_menu(name, yes="Согласиться", no="Отказаться"):
    builder = InlineKeyboardBuilder()
    builder.row(*[
        InlineKeyboardButton(text=yes, callback_data=f"{name}_1"),
        InlineKeyboardButton(text=no, callback_data=f"{name}_0"),
    ],
    width=1
    )

    return builder.as_markup()