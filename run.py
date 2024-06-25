import asyncio
import subprocess
import threading

from loader import bot, dp
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

def run_fastapi():
    command = f"uvicorn my_site:app --host 0.0.0.0 --port $PORT"
    subprocess.run(command, shell=True)


if __name__ == '__main__':
    try:
        fastapi_thread = threading.Thread(target=run_fastapi)
        fastapi_thread.start()
        print('Site started!')

        asyncio.run(run())
        print('Bot started!')
    except KeyboardInterrupt:
        print('Bot stopped!')
