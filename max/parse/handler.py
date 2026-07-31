from maxapi.types import MessageCreated
from maxapi.context import MemoryContext
from core.config import bot
import bot.parse.parsing as parsing_service
import asyncio


async def start_parse_task(event: MessageCreated, state: MemoryContext):
    data = await state.get_data()
    if data.get("parser_task") and not data["parser_task"].done():
        await event.message.answer("Парсинг уже запущен!")
    else:
        task = asyncio.create_task(
            parsing_service.parse_projects_and_send(bot, event.chat.chat_idZ, state)
        )
        await state.update_data(parser_task=task)
        await event.message.answer("Парсинг запущен!")


async def stop_parse_task(event: MessageCreated, state: MemoryContext):
    data = await state.get_data()
    task = data.get("parser_task")
    if task and not task.done():
        task.cancel()
        await event.message.answer("Парсинг остановлен!")
    else:
        await event.message.answer("Парсинг не был запущен или уже завершён.")
