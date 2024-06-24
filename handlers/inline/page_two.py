from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline.book_gifts import select_segment, select_gift, open_gift_kb, open_booked_gifts_kb, open_booked_gift_kb, info, admin_kb
from keyboards.inline.start_kb import start_menu
from config import VERSION

from loader import base

router = Router()

@router.callback_query(F.data.startswith('menu'))
async def page_two(call_data: CallbackQuery):
    if call_data.data == 'menu_gifts_list':
        await call_data.message.edit_text(text='Выберите желаемый сегмент подарков', reply_markup=select_segment())
        await call_data.answer()

    elif call_data.data == 'menu_my_book':
        gifts = await base.get_booked_gifts(id_user=call_data.from_user.id)

        await call_data.message.edit_text(
            text='Ниже указаны подарки, которые вы забронировали. Вы можете узнать подробности, провалившись внутрь подарка, нажав на кнопку!',
            reply_markup=open_booked_gifts_kb(gifts=gifts)
        )

    elif call_data.data == 'menu_info':
        await call_data.message.edit_text(
            text=f'Версия бота: {VERSION}',
            reply_markup=info()
        )

    elif call_data.data == 'menu_admin':
        await call_data.message.edit_text(
            text=f'Выберите подарок для редактирования или удаления или добавите новый!', 
            reply_markup=await admin_kb()
        )

@router.callback_query(F.data.startswith('SS'))
async def print_gifts(call_data: CallbackQuery):

    segment = call_data.data.removeprefix('SS_')

    await call_data.message.edit_text(text='Выберите желаемый подарок. Для получения более подробной информации, перейдите в тело подарка, нажав на него, где вы можете его забронировать.\n\n‼️Если рядом с подарком стоит значек "🔒", то он забронирован‼️', reply_markup=await select_gift(segment=segment))
    await call_data.answer()

@router.callback_query(F.data.startswith('SG'))
async def print_gifts(call_data: CallbackQuery):
    id_gift = call_data.data.removeprefix('SG_')

    data = await base.get_gift(id=id_gift)

    if data[3] != 'book':
        await call_data.message.edit_text(
            text=f'Название: {data[1]}\nЦена: {data[2]} вечно деревянных\nОписание: {data[4]}\n\nСтатус: {"Забронированно🔒" if data[-1] != 0 else "Доступно✅"}\n\nНиже представлены ссылки, где можно купить данный подарок (если их нет, значит мне лень было их давать🤷🏼‍♂️ или я не смог это сделать)', 
            reply_markup=open_gift_kb(id_gift=id_gift, links=data[5].split('|'), book_status=data[-1])
        )

    else:
        await call_data.message.edit_text(
            text=f'Название: {data[1]}\nАвтор: {data[2]}\nОписание: {data[4]}\n\nСтатус: {"Забронированно🔒" if data[-1] != 0 else "Доступно✅"}', 
            reply_markup=open_gift_kb(id_gift=id_gift, book_status=data[-1])
        )

    await call_data.answer()

@router.callback_query(F.data.startswith('OG'))
async def process_gift(call_data: CallbackQuery):
    name_process = call_data.data.removeprefix('OG_')

    if 'booked' in name_process:
        id_gift = name_process.split('_')[-1]

        await base.add_booked_user(id_user=call_data.from_user.id, id_gift=id_gift)
        await call_data.answer('Забронированно! Теперь оно появится в забронированных в главном меню!')
        await call_data.message.edit_text(text='Выберите желаемый сегмент подарков', reply_markup=select_segment())

    elif name_process == 'null':
        await call_data.answer()

    elif name_process == 'back':
        await call_data.message.edit_text(text='Выберите желаемый сегмент подарков', reply_markup=select_segment())

    elif name_process == 'home':
        await call_data.message.edit_text(text=f'Выберите нужный пункт из меню ниже', reply_markup=await start_menu(id=call_data.from_user.id))

@router.callback_query(F.data.startswith('AGS'))
async def process_gift(call_data: CallbackQuery):
    id_gift = call_data.data.removeprefix('AGS_')

    data = await base.get_gift(id=id_gift)

    if data[3] != 'book':
        await call_data.message.edit_text(
                text=f'Название: {data[1]}\nЦена: {data[2]} вечно деревянных\nОписание: {data[4]}\n\nНиже представлены ссылки, где можно купить данный подарок (если их нет, значит мне лень было их давать🤷🏼‍♂️ или я не смог это сделать)', 
                reply_markup=open_booked_gift_kb(id_gift=id_gift, links=data[5].split('|'))
            )
        
    else:
        await call_data.message.edit_text(
                text=f'Название: {data[1]}\nАвтор: {data[2]}\nОписание: {data[4]}', 
                reply_markup=open_booked_gift_kb(id_gift=id_gift)
            )
    
    await call_data.answer()

@router.callback_query(F.data.startswith('AG'))
async def process_gift(call_data: CallbackQuery):
    request = call_data.data.removeprefix('AG_')

    if 'unbook' in request:
        await base.remove_booked_user(id_gift=request.split('_')[-1])
        await call_data.message.edit_text(text=f'Выберите нужный пункт из меню ниже', reply_markup=await start_menu(id=call_data.from_user.id)) 
        await call_data.answer('Вы разбронировали этот подарок и теперь он доступен для брони в меню выбора подарков.')
        