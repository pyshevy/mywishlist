from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline.book_gifts import open_gift_admin
from keyboards.inline.start_kb import start_menu
from keyboards.inline.conf_kb import conf_menu
from config import VERSION

from loader import base

router = Router()

@router.callback_query(F.data.startswith('APF'))
async def get_gift(call_data: CallbackQuery):
    id_gift = call_data.data.removeprefix('APF_')

    data = await base.get_gift(
        id=id_gift
    )

    if data[3] != 'book':
        await call_data.message.edit_text(
            text=f'Название: {data[1]}\nЦена: {data[2]} вечно деревянных\nОписание: {data[4]}\n\nСтатус: {"Забронированно🔒" if data[-1] != 0 else "Доступно✅"}', 
            reply_markup=open_gift_admin(id_gift=id_gift, links=data[5].split('|'), name=data[1], price=data[2], desc=data[4], price_segment=data[3])
        )

    else:
        await call_data.message.edit_text(
            text=f'Название: {data[1]}\nАвтор: {data[2]}\nОписание: {data[4]}\n\nСтатус: {"Забронированно🔒" if data[-1] != 0 else "Доступно✅"}', 
            reply_markup=open_gift_admin(id_gift=id_gift, links=data[5].split('|'), name=data[1], price=data[2], desc=data[4], price_segment=data[3])
        )

    await call_data.answer()

@router.callback_query(F.data.startswith('APD'))
async def delete_gift(call_data: CallbackQuery):
    request = call_data.data.removeprefix('APD_')

    if 'delete' in request:
        await call_data.message.edit_text(
            text='Подтвердите удаление',
            reply_markup=conf_menu(
                name=f'APD_{request.split("_")[-1]}',
                yes='Подтвердить',
                no="Отменить"
            )
        )

    else:
        if int(request.split('_')[-1]):
            await base.remove_gift(id=int(request.split('_')[0]))
            await call_data.answer('Успешно удалено!')
            await call_data.message.edit_text(text=f'Выберите нужный пункт из меню ниже', reply_markup=await start_menu(id=call_data.from_user.id))

        else:
            await call_data.answer('Успешно отменено!')
            await call_data.message.edit_text(text=f'Выберите нужный пункт из меню ниже', reply_markup=await start_menu(id=call_data.from_user.id))
        