import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from core.config import settings
from bot.routers import router

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    bot = Bot(
        token=settings.telegram_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    print("Starting aiogram Telegram bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
