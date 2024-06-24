import asyncio

from loader import bot, dp
from my_site import keep_alive
import os

from handlers import (
    start_router,
    delete_text,
    router_page_two,
    admin_router
)


async def run() -> None:
    dp.include_routers(start_router, router_page_two, admin_router, delete_text)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, )

def onstartup():
    print('Bot started!')
    print(os.path.abspath(__file__))
    keep_alive()
    asyncio.run(run())

def shutdown():
    print('Bot stopped!')


if __name__ == '__main__':
    dp.startup.register(onstartup())
    dp.shutdown.register(shutdown())
