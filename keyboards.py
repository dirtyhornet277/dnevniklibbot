from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup()
buttons = ["Узнать дз", "Узнать оценки"]
for i in buttons:
    keyboard.add(KeyboardButton(i))
