from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


current_location = ReplyKeyboardMarkup([
    [KeyboardButton(text='Отправить текущую 📍', request_location=True)]
], resize_keyboard=True)
