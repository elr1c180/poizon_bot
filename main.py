import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, get_promo, admin, cancel

async def main():
    bot = Bot(token="")
    dp = Dispatcher()

    dp.include_routers(start.router, get_promo.router, admin.router, cancel.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
