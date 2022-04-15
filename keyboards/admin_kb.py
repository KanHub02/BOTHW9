from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_upload = KeyboardButton('/upload')
button_cancel = KeyboardButton('/cancel')

button_admin = ReplyKeyboardMarkup(
    resize_keyboard=True).row(button_upload, button_cancel)