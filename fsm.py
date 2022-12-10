from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class DateM(StatesGroup):
    day = State()
    month = State()
    year = State()

class DateHW(StatesGroup):
    day = State()
    month = State()
    year = State()