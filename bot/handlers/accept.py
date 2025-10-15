from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states import OfferStates
from bot.services.offer import (
    handle_offer_price,
    handle_offer_term,
    handle_offer_comment,
)
from core.config import settings

router = Router()


@router.message(OfferStates.waiting_for_price)
async def accept_price(message: Message, state: FSMContext):
    if message.from_user.id != settings.allowed_user_id:
        return
    await handle_offer_price(message, state)


@router.message(OfferStates.waiting_for_term)
async def accept_term(message: Message, state: FSMContext):
    if message.from_user.id != settings.allowed_user_id:
        return
    await handle_offer_term(message, state)


@router.message(OfferStates.waiting_for_comment)
async def accept_comment(message: Message, state: FSMContext):
    if message.from_user.id != settings.allowed_user_id:
        return
    await handle_offer_comment(message, state)
