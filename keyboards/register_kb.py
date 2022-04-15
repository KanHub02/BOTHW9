from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_register = KeyboardButton('/register')
button_cancel = KeyboardButton('/canceluser')

button_admin_register = ReplyKeyboardMarkup(
    resize_keyboard=True).row(button_register, button_cancel)
