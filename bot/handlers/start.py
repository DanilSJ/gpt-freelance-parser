from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from core.config import settings

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    if message.from_user.id != settings.allowed_user_id:
        return
    await message.answer(
        "Добро пожаловать в бот!\nКоманды:\n/parserun – начать парсинг\n/parsestop – остановить парсинг"
    )


@router.message(Command("parserun"))
async def parserun_cmd(message: Message, state: FSMContext):
    if message.from_user.id != settings.allowed_user_id:
        return
    from bot.handlers.parse import start_parse_task

    await start_parse_task(message, state)


@router.message(Command("parsestop"))
async def parsestop_cmd(message: Message, state: FSMContext):
    if message.from_user.id != settings.allowed_user_id:
        return
    from bot.handlers.parse import stop_parse_task

    await stop_parse_task(message, state)
