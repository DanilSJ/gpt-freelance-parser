from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.config import bot
import asyncio


async def start_parse_task(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("parser_task") and not data["parser_task"].done():
        await message.answer("Парсинг уже запущен!")
    else:
        import bot.services.parsing as parsing_service

        task = asyncio.create_task(
            parsing_service.parse_projects_and_send(bot, message.chat.id, state)
        )
        await state.update_data(parser_task=task)
        await message.answer("Парсинг запущен!")


async def stop_parse_task(message: Message, state: FSMContext):
    data = await state.get_data()
    task = data.get("parser_task")
    if task and not task.done():
        task.cancel()
        await message.answer("Парсинг остановлен!")
    else:
        await message.answer("Парсинг не был запущен или уже завершён.")
