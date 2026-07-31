from maxapi import Router
from maxapi.types import Message
from maxapi.types import Command, CommandStart
from maxapi.context import MemoryContext
from max.parse.handler import start_parse_task, stop_parse_task

router = Router()


@router.message_created(CommandStart())
async def start_cmd(message: Message):
    return await message.answer(
        "Добро пожаловать в бот!\nКоманды:\n/parserun – начать парсинг\n/parsestop – остановить парсинг"
    )


@router.message_created(Command("parserun"))
async def parserun_cmd(message: Message, state: MemoryContext):
    return await start_parse_task(message, state)


@router.message_created(Command("parsestop"))
async def parsestop_cmd(message: Message, state: MemoryContext):
    return await stop_parse_task(message, state)
