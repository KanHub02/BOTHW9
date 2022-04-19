from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

help_button = KeyboardButton("/help")
quiz_button = KeyboardButton("/quiz")
Brain_up_button = KeyboardButton('/BrainUp')
brainnext_button = KeyboardButton('/BrainNext')
cat_up = KeyboardButton('/cat')
user_button = KeyboardButton('/users')

location_button = KeyboardButton("Share Location", request_location=True)
info_button = KeyboardButton("Share Info", request_contact=True)

start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

start_markup.row(help_button, quiz_button,
                 location_button, info_button,
                 Brain_up_button, brainnext_button,
                 cat_up, user_button)
