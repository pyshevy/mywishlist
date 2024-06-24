from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

from loader import base


def select_segment():
    builder = InlineKeyboardBuilder()
    builder.row(*[
        InlineKeyboardButton(text="Книги", callback_data="SS_book"),
        InlineKeyboardButton(text="Маленькие подарочки (обычно до 1000)", callback_data="SS_mini"),
        InlineKeyboardButton(text="Средние (до 5000)", callback_data="SS_medium"),
        InlineKeyboardButton(text="Днерожденевские (покрупнее)", callback_data="SS_big"),
        InlineKeyboardButton(text="----------------", callback_data="OG_null"),
        InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home")
    ],
    width=1
    )

    return builder.as_markup()

async def select_gift(segment: str):
    gifts = await base.get_gifts(segment=segment)

    kb = []

    if gifts:
        for gift in gifts:
            kb.append(InlineKeyboardButton(text=f"{gift[1]} {'🔒' if gift[-1] != 0 else ''}", callback_data=f"SG_{gift[0]}"))

    else:
        kb.append(InlineKeyboardButton(text="Пока тут ничего нет, но я скоро добавлю сюда подарки!", callback_data="OG_null"))
    
    kb.append(InlineKeyboardButton(text="----------------", callback_data="OG_null"))
    kb.append(InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home"))
    builder = InlineKeyboardBuilder()
    builder.row(*kb, width=1)
    return builder.as_markup()

def open_gift_kb(id_gift, book_status, links: list = []):
    builder = InlineKeyboardBuilder()
    kb = []
    
    if links and links[0]:
        for link in links:
            kb.append(InlineKeyboardButton(text="Перейти", url=link))

        if book_status != 0:
            kb.append(InlineKeyboardButton(text="----------------", callback_data="OG_null"))
            kb.append(InlineKeyboardButton(text="🔴Забронированно🔴", callback_data="OG_null"))
            
        else:
            kb.append(InlineKeyboardButton(text="Забронировать📥", callback_data=f"OG_booked_{id_gift}"))

        kb.append(InlineKeyboardButton(text="Назад🧳", callback_data="OG_back"))
        kb.append(InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home"))

    else:
        if book_status != 0:
            kb.append(InlineKeyboardButton(text="----------------", callback_data="OG_null"))
            kb.append(InlineKeyboardButton(text="🔴Забронированно🔴", callback_data="OG_null"))
        else:
            kb.append(InlineKeyboardButton(text="Забронировать📥", callback_data=f"OG_booked_{id_gift}")) 

        kb.append(InlineKeyboardButton(text="Назад🧳", callback_data="OG_back"))
        kb.append(InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home"))

    builder.row(*kb, width=1)
    return builder.as_markup()

def open_booked_gifts_kb(gifts: list):
    builder = InlineKeyboardBuilder()
    kb = []

    for gift in gifts:
        kb.append(InlineKeyboardButton(text=f"{gift[1]}", callback_data=f"AGS_{gift[0]}"))

    kb.append(InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home"))

    builder.row(*kb, width=1)
    return builder.as_markup()

def open_booked_gift_kb(id_gift, links: list = []):
    builder = InlineKeyboardBuilder()
    kb = []

    if links and links[0]:
        for link in links:
                kb.append(InlineKeyboardButton(text="Перейти", url=link))

        kb.append(InlineKeyboardButton(text="----------------", callback_data="OG_null"))

    kb.append(InlineKeyboardButton(text="Разбронировать📤", callback_data=f"AG_unbook_{id_gift}"))
    kb.append(InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home"))

    builder.row(*kb, width=1)
    return builder.as_markup()

def info():
    builder = InlineKeyboardBuilder()

    builder.row(*[
        InlineKeyboardButton(text="Телеграмм разработчика", url='tg://user?id=1158687926'),
        InlineKeyboardButton(text="----------------", callback_data="OG_null"),
        InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home")
    ], 
    width=1
    )
    return builder.as_markup()

async def admin_kb():
    builder = InlineKeyboardBuilder()
    kb = []
    count = await base.get_count_gifts()

    gifts = await base.get_all_gifts()

    for gift in gifts:
        kb.append(InlineKeyboardButton(text=f"{gift[1]} {'🔒' if gift[-1] != 0 else ''}", callback_data=f"APF_{gift[0]}"))

    kb.append(InlineKeyboardButton(text="----------------", callback_data="OG_null"))
    kb.append(InlineKeyboardButton(text=f"Добавить📝", web_app=WebAppInfo(url=f'https://mywishlist-t9ny.onrender.com/form?task=add&id_gift={count+1}')))
    kb.append(InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home"))

    builder.row(*kb, width=1)
    return builder.as_markup()

def open_gift_admin(id_gift, links, name, price, desc, price_segment):
    builder = InlineKeyboardBuilder()
    kb = []

    if links and links[0]:
        for link in links:
            kb.append(InlineKeyboardButton(text="Перейти", url=link))

        kb.append(InlineKeyboardButton(text="----------------", callback_data="OG_null"))

    kb.append(InlineKeyboardButton(text="Изменить✏️", web_app=WebAppInfo(url=f"https://mywishlist-t9ny.onrender.com/form?task=edit&title={name}&price={price}&description={desc}&price_segment={price_segment}&id_gift={id_gift}")))
    kb.append(InlineKeyboardButton(text="Удалить🗑", callback_data=f"APD_delete_{id_gift}"))
    kb.append(InlineKeyboardButton(text="В главное меню🏠", callback_data="OG_home"))

    builder.row(*kb, width=1)
    return builder.as_markup()
