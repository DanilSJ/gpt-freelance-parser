from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.parse.offer import request_offer_comment, regenerate_ai_response, start_offer_flow
from core.config import settings


router = Router()


@router.callback_query(F.data.startswith("accept_"))
async def on_accept(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != settings.allowed_user_id:
        return
    await callback.answer()
    await start_offer_flow(callback, state)


@router.callback_query(F.data.startswith("reject_"))
async def on_reject(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != settings.allowed_user_id:
        return
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith("regen_"))
async def on_regen(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != settings.allowed_user_id:
        return
    await callback.answer("Генерация отклика...", show_alert=False)  # Сразу!

    await regenerate_ai_response(callback, state)


@router.callback_query(F.data.startswith("comment_"))
async def on_comment(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != settings.allowed_user_id:
        return
    await callback.answer()

    await request_offer_comment(callback, state)
