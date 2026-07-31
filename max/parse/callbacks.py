from maxapi import Router, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext
from max.parse.offer import request_offer_comment, regenerate_ai_response, start_offer_flow
from core.config import settings


router = Router()


@router.message_callback(F.data.startswith("accept_"))
async def on_accept(callback: MessageCallback, state: MemoryContext):
    if callback.from_user.id != settings.allowed_user_id:
        return
    await callback.answer()
    await start_offer_flow(callback, state)


@router.message_callback(F.data.startswith("reject_"))
async def on_reject(callback: MessageCallback, state: MemoryContext):
    if callback.from_user.id != settings.allowed_user_id:
        return
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@router.message_callback(F.data.startswith("regen_"))
async def on_regen(callback: MessageCallback, state: MemoryContext):
    if callback.from_user.id != settings.allowed_user_id:
        return
    await callback.answer("Генерация отклика...")

    await regenerate_ai_response(callback, state)


@router.message_callback(F.data.startswith("comment_"))
async def on_comment(callback: MessageCallback, state: MemoryContext):
    if callback.from_user.id != settings.allowed_user_id:
        return
    await callback.answer()

    await request_offer_comment(callback, state)
