from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    get_idea = State()
    get_problem = State()
