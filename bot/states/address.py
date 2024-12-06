from aiogram.dispatcher.filters.state import State, StatesGroup

class Address(StatesGroup):
    address_code = State() 
    location = State()