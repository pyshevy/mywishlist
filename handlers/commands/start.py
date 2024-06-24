from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.inline.conf_kb import conf_menu
from keyboards.inline.start_kb import start_menu

from loader import base

router = Router()

class Message_id(StatesGroup):
    message_id = State()

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if not (await base.get_user(id=message.from_user.id)):
        docs = FSInputFile('docs/Соглашение.docx')
        await message.answer_document(document=docs, caption=f'Здравствуйте, {message.from_user.full_name}! Чтобы использовать бота, примите пользовательское соглашение! (Оно прикреплено к сообщению!)', reply_markup=conf_menu('docs'))
        await state.set_state(Message_id.message_id)
        await state.update_data(message_id=message.message_id+1)

    else:
        await message.answer(f'Здравствуй, {message.from_user.full_name}!\nВыберите нужный пункт из меню ниже', reply_markup=await start_menu(id=message.from_user.id))

@router.callback_query(F.data.startswith('docs'), Message_id.message_id)
async def conf_docs(call_data: CallbackQuery, state: FSMContext):
    message_id = await state.get_data()
    request = call_data.data.removeprefix('docs_')

    await call_data.bot.delete_message(chat_id=call_data.message.chat.id, message_id=message_id.get('message_id'))

    if int(request):
        await base.add_user(
            id=call_data.from_user.id,
            username=call_data.from_user.username,
            url=call_data.from_user.url
        )

        await call_data.message.answer(f'Спасибо, {call_data.from_user.full_name}! Удачного использования!\n\nВыберите нужный пункт из меню ниже', reply_markup=await start_menu(id=call_data.from_user.id))

    else:
        await call_data.message.answer('В таком случае вы не можете пользоваться ботом! Отправьте /start, чтобы начать заново')

    await call_data.answer()
