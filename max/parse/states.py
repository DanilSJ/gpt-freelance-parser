from maxapi.context import State, StatesGroup

class OfferStates(StatesGroup):
    waiting_for_comment = State()
    waiting_for_price = State()
    waiting_for_term = State()
