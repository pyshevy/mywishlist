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


if __name__ == '__main__':
    try:
        print('Bot started!')
        asyncio.run(run())
        keep_alive()
    except KeyboardInterrupt:
        print('Bot stopped!')
