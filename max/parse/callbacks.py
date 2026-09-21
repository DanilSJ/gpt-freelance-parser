from maxapi import Router, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext
from max.parse.offer import request_offer_comment, regenerate_ai_response, start_offer_flow

router = Router()


@router.message_callback(F.callback.payload.startswith("accept_"))
async def on_accept(callback: MessageCallback, context: MemoryContext):
    print("dwdwwddw")
    await start_offer_flow(callback, context)


@router.message_callback(F.callback.payload.startswith("reject_"))
async def on_reject(callback: MessageCallback, context: MemoryContext):
    print("xxewqxdewfdewfe")
    await callback.message.delete()


@router.message_callback(F.callback.payload.startswith("regen_"))
async def on_regen(callback: MessageCallback, context: MemoryContext):
    await callback.answer("Генерация отклика...")

    await regenerate_ai_response(callback, context)


@router.message_callback(F.callback.payload.startswith("comment_"))
async def on_comment(callback: MessageCallback, context: MemoryContext):
    await callback.answer()

    await request_offer_comment(callback, context)
