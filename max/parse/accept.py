from maxapi import Router
from maxapi.types import MessageCreated
from maxapi.context import MemoryContext
from max.parse.states import OfferStates
from max.parse.offer import (
    handle_offer_price,
    handle_offer_term,
    handle_offer_comment,
)

router = Router()


@router.message_created(OfferStates.waiting_for_price)
async def accept_price(event: MessageCreated, context: MemoryContext):
    return await handle_offer_price(event, context)


@router.message_created(OfferStates.waiting_for_term)
async def accept_term(event: MessageCreated, context: MemoryContext):
    return await handle_offer_term(event, context)


@router.message_created(OfferStates.waiting_for_comment)
async def accept_comment(event: MessageCreated, context: MemoryContext):
    return await handle_offer_comment(event, context)
