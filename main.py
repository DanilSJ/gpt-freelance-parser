import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from core.config import settings
from bot.routers import router

async def Telegram():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    bot = Bot(
        token=settings.telegram_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    print("Starting aiogram Telegram bot...")
    await dp.start_polling(bot)

async def Max():
    pass

async def main():
    if settings.Telegram:
        await Telegram()

    if settings.Max:
        await Max()

if __name__ == "__main__":
    asyncio.run(main())
