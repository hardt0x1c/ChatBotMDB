from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    admin_spam = State()
