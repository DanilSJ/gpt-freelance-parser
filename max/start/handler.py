from maxapi import Router
from maxapi.types import MessageCreated
from maxapi.types import Command, CommandStart
from maxapi.context import MemoryContext
from max.parse.handler import start_parse_task, stop_parse_task

router = Router()


@router.message_created(CommandStart())
async def start_cmd(event: MessageCreated):
    return await event.message.answer(
        "Добро пожаловать в бот!\nКоманды:\n/parserun – начать парсинг\n/parsestop – остановить парсинг"
    )


@router.message_created(Command("parserun"))
async def parserun_cmd(event: MessageCreated, context: MemoryContext):
    return await start_parse_task(event, context)


@router.message_created(Command("parsestop"))
async def parsestop_cmd(event: MessageCreated, context: MemoryContext):
    return await stop_parse_task(event, context)
