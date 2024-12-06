from aiogram.dispatcher.filters.state import State, StatesGroup

class Accept(StatesGroup):
    order_id = State() 
    date = State()
class Cancel(StatesGroup):
    order_id = State()
    reason = State()