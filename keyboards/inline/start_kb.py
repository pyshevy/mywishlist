from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.database import UserBase
from loader import base
from config import ID_ADMIN

base: UserBase

async def start_menu(id):
    booked_gifts = await base.get_booked_gifts(id_user=id)

    builder = InlineKeyboardBuilder()

    if booked_gifts:
        builder.row(*[
            InlineKeyboardButton(text="Список подарков", callback_data="menu_gifts_list"),
            InlineKeyboardButton(text="Ваши брони", callback_data="menu_my_book"),
            InlineKeyboardButton(text="Информация", callback_data="menu_info")
        ],
        width=1
        )

    else:
        builder.row(*[
            InlineKeyboardButton(text="Список подарков", callback_data="menu_gifts_list"),
            InlineKeyboardButton(text="Информация", callback_data="menu_info")
        ],
        width=1
        )

    if id == ID_ADMIN:
        builder.add(InlineKeyboardButton(text="Редактирование и просмотр", callback_data="menu_admin"))

    return builder.as_markup()

