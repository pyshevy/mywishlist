from aiogram import Dispatcher, Bot, Router
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.client.session.aiohttp import AiohttpSession

from db.database import UserBase

from config import TOKEN

dp = Dispatcher(storage=MemoryStorage())
base: UserBase = UserBase('db.db')

# if PLACE_OF_LAUNCH == 1:
#     session = AiohttpSession(proxy='http://proxy.server:3128')
#     bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML, session=session)

# else:
#     bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

bot = Bot(token=TOKEN)

router = Router()



