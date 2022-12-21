from dnevniklib import *
from aiogram import types, Bot, Dispatcher, executor
from settings import *
from keyboards import keyboard
from fsm import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
user = User(token=token_mos)
marks = Marks(user.session, user.token, user.id)
homeworks = Homeworks(user.session, user.token, user.id)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    if str(msg.from_user.id) == userid:
        await msg.answer("Hello, Ivan!", reply_markup=keyboard)

@dp.message_handler(content_types=["text"])
async def get_marks(msg: types.Message):
    if str(msg.from_user.id) == userid:
        if msg.text == "Узнать оценки":
            keyboard_day = ReplyKeyboardMarkup()
            for i in range(1, 32):
                keyboard_day.add(KeyboardButton(i))
            await msg.answer("Выберите день", reply_markup=keyboard_day)
            await DateM.day.set()
        if msg.text == "Узнать дз":
            keyboard_day = ReplyKeyboardMarkup()
            for i in range(1, 32):
                keyboard_day.add(KeyboardButton(i))
            await msg.answer("Выберите день", reply_markup=keyboard_day)
            await DateHW.day.set()

@dp.message_handler(state=DateM.day)
async def day_set(msg:types.Message, state: FSMContext):
    await state.update_data(day=msg.text)
    keyboard_month = ReplyKeyboardMarkup()
    for i in range(1, 13):
        keyboard_month.add(KeyboardButton(i))
    await msg.answer("Выберите месяц", reply_markup=keyboard_month)
    await DateM.next()
@dp.message_handler(state=DateM.month)
async def month_set(msg:types.Message, state: FSMContext):
    await state.update_data(month=msg.text)
    keyboard_year = ReplyKeyboardMarkup()
    for i in range(2021, 2023):
        keyboard_year.add(KeyboardButton(i))
    await msg.answer("Выберите год", reply_markup=keyboard_year)
    await DateM.next()

@dp.message_handler(state=DateM.year)
async def year_set(msg:types.Message, state: FSMContext):
    await state.update_data(year=msg.text)
    user_data = await state.get_data()
    message = f"Оценки на {user_data['day']}.{user_data['month']}.{user_data['year']}\n\n\n"
    try:
        my_mark = marks.get_marks_by_data(user.get_date_in_format(year=user_data["year"], month=user_data["month"], date=user_data["day"]))
        print(my_mark)
        if my_mark == []:
            message = message + "нет"
        else:
            for mark in my_mark:
                print(mark)
                message = message + f"{mark['name']}: <b>{mark['mark']}</b>\n"
        await msg.answer(message, parse_mode="html", reply_markup=keyboard)
        await state.finish()
    except DnevnikLibError:
        await msg.answer("Извините, походу неверная дата", reply_markup=keyboard)
        await  state.finish()

@dp.message_handler(state=DateHW.day)
async def day_set(msg:types.Message, state: FSMContext):
    await state.update_data(day=msg.text)
    keyboard_month = ReplyKeyboardMarkup()
    for i in range(1, 13):
        keyboard_month.add(KeyboardButton(i))
    await msg.answer("Выберите месяц", reply_markup=keyboard_month)
    await DateHW.next()
@dp.message_handler(state=DateHW.month)
async def month_set(msg:types.Message, state: FSMContext):
    await state.update_data(month=msg.text)
    keyboard_year = ReplyKeyboardMarkup()
    for i in range(2021, 2023):
        keyboard_year.add(KeyboardButton(i))
    await msg.answer("Выберите год", reply_markup=keyboard_year)
    await DateHW.next()

@dp.message_handler(state=DateHW.year)
async def year_set(msg:types.Message, state: FSMContext):
    await state.update_data(year=msg.text)
    user_data = await state.get_data()
    message = f"ДЗ на {user_data['day']}.{user_data['month']}.{user_data['year']}\n\n\n"
    try:
        my_hw = homeworks.get_homeworks_by_data(user.get_date_in_format(year=user_data["year"], month=user_data["month"], date=user_data["day"]))
        print(my_hw)
        if my_hw == []:
            message = message + "нет"
        else:
            for hw in my_hw:
                print(hw)
                message = message + f"{hw['name']}: <b>{hw['homework']}</b>\n"
        await msg.answer(message, parse_mode="html", reply_markup=keyboard)
        await state.finish()
    except DnevnikLibError:
        await msg.answer("Извините, походу неверная дата", reply_markup=keyboard)
        await  state.finish()



executor.start_polling(dispatcher=dp)
