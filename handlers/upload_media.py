from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from database import bot_db


class Library(StatesGroup):
    photo = State()
    types = State()
    file_name = State()


async def starter(message: types.message):
    global ADMIN_ID
    ADMIN_ID = message.from_user.id
    await bot.send_message(message.from_user.id,
                           "Here you can upload your media to use after", )


async def cancel_command(message: types.Message,
                         state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return "State is None, Relax"
    await state.finish()
    await message.reply("Canceled Successfully")


async def add_start(message: types.Message):
    await Library.photo.set()
    await message.reply("Send me photo")


async def load_photo(message: types.Message,
                     state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await Library.next()
    await message.reply("File Name")


async def load_file_name(message: types.Message,
                         state: FSMContext):
    async with state.proxy() as data:
        data['file_name'] = message.text
    await Library.next()
    await message.reply("Added")
    await bot_db.sql_insert(state)
    await state.finish()

async def get_library(message: types.Message):
    await bot_db.media_select(message)

def register_handler_media(dp: Dispatcher):
    dp.register_message_handler(starter, commands=['library'])
    dp.register_message_handler(cancel_command, commands=['canceladd'])
    dp.register_message_handler(add_start, commands=['add'])
    dp.register_message_handler(get_library, commands=['showme'])
