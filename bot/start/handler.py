from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from bot.parse.handler import start_parse_task, stop_parse_task
from core.config import settings

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    if message.from_user.id != settings.allowed_user_id:
        return
    await message.answer(
        "Добро пожаловать в бот!\nКоманды:\n/parserun – начать парсинг\n/parsestop – остановить парсинг"
    )


@router.message(Command("parserun"))
async def parserun_cmd(message: Message, state: FSMContext):
    if message.from_user.id != settings.allowed_user_id:
        return

    await start_parse_task(message, state)


@router.message(Command("parsestop"))
async def parsestop_cmd(message: Message, state: FSMContext):
    if message.from_user.id != settings.allowed_user_id:
        return

    await stop_parse_task(message, state)
