import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from core.config import settings
from bot.routers import router as telegram_router
from max.routers import router as max_router

from maxapi import Bot as MaxBot, Dispatcher as MaxDispatcher

async def Telegram():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(telegram_router)
    bot = Bot(
        token=settings.telegram_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    print("Starting Telegram bot...")
    await dp.start_polling(bot)

async def Max():
    bot = MaxBot(token=settings.max_token)
    dp = MaxDispatcher()
    dp.include_routers(max_router)

    print("Starting Max bot...")
    await dp.start_polling(bot)

async def main():
    tasks = []

    if settings.Telegram:
        tasks.append(asyncio.create_task(Telegram()))

    if settings.Max:
        tasks.append(asyncio.create_task(Max()))

    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("No bots enabled!")

if __name__ == "__main__":
    asyncio.run(main())
