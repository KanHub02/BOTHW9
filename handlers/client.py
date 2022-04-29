from aiogram import types, Dispatcher
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import client_kb
from config import bot
from database import bot_db
from ParsHandler import pars


async def hello(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Hello {message.from_user.first_name} here I can scare, update and make laugh your brain",
                           reply_markup=client_kb.start_markup)


async def help(message: types.Message):
    await message.reply("1. /quiz command will start quiz series of problems\n"
                        "2./BrainNext command tap our amazing world!\n"
                        "3./cat command you must see it\n"
                        "4./help1 more info!"
                        "Or just press button"
                        "Whenever you press Следующая Викторина will appear next quiz\n"
                        "Note: Bot-Admin will delete cursed words, so that's why be careful")


async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("Следующая Викторина",
                                         callback_data="button_call_1")
    markup.add(button_call_1)
    question = "How old is Putin"
    answers = [
        "50+", "60+", "70+", "80+", "Immortal"
    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        explanation="This is a joke",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup,
    )


async def cat(message: types.Message):
    video = open('media/cat.mp4', 'rb')
    await bot.send_video(message.chat.id, video)
    await bot.send_message(message.chat.id, '__,,,^._.^,,,__')


async def brainup(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Чёрная дыра́ — область пространства-времени, гравитационное притяжение которой настолько велико, что покинуть её не могут даже фотоны')


async def brain_quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_5 = InlineKeyboardButton("M  Y  S  T  E  R  Y ",
                                         callback_data="button_call_5")
    button_call_6 = InlineKeyboardButton("S   P   A   C   E",
                                         callback_data="button_call_6")
    markup.add(button_call_5, button_call_6)
    await bot.send_message(message.chat.id, 'Что тебе интересно?',
                           reply_markup=markup)


async def get_all_tvshow(message: types.Message):
    await bot_db.sql_select(message)


async def get_all_users(message: types.Message):
    await bot_db.user_select(message)


async def parser_link(message: types.Message):
    data = pars.scrapy_script()
    await bot.send_message(message.chat.id, data)


async def parser_title(message: types.Message):
    data = pars.scrapy_script_title()
    await bot.send_message(message.chat.id, data)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(hello, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(brainup, commands=['BrainUp'])
    dp.register_message_handler(brain_quiz_1, commands=['BrainNext'])
    dp.register_message_handler(cat, commands=['cat'])
    dp.register_message_handler(get_all_tvshow, commands=['twshow'])
    dp.register_message_handler(get_all_users, commands=['getusers'])
    dp.register_message_handler(parser_link, commands=['news'])
    dp.register_message_handler(parser_title, commands=['title'])
