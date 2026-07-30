from aiogram.fsm.state import StatesGroup, State

class OfferStates(StatesGroup):
    waiting_for_comment = State()
    waiting_for_price = State()
    waiting_for_term = State()
