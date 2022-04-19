from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import bot_db
from keyboards import register_kb
from config import bot


class FSM_USER_REGISRER(StatesGroup):
    photo = State()
    id = State()
    username = State()
    first_name = State()
    last_name = State()


async def is_user_register_command(message: types.Message):
    global ID
    ID = message.chat.id
    await bot.send_message(message.chat.id,
                           "Yes, User\n"
                           "Sign up for bot",
                           reply_markup=register_kb.button_register)
    await message.delete()


async def cancel_command(message: types.Message,
                         state: FSMContext):
    if message.chat.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return "State is None, Relax"
        await state.finish()
        await message.reply("Canceled Successfully")


async def fsm_start(message: types.Message):
    if message.chat.id == ID:
        await FSM_USER_REGISRER.photo.set()
        await message.reply("User, Send me photo please")


async def load_photo(message: types.Message,
                     state: FSMContext):
    async with state.proxy() as info:
        info['photo'] = message.photo[0].file_id
    await FSM_USER_REGISRER.next()


async def load_id(message: types.Message,
                  state: FSMContext):
    async with state.proxy() as info:
        info['id'] = message.chat.id
    await FSM_USER_REGISRER.next()
    await message.reply("User, Send me your username please")


async def load_username(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as info:
        info['username'] = message.text
    await FSM_USER_REGISRER.next()
    await message.reply("User, Send me your first_name please")


async def load_first_name(message: types.Message,
                          state: FSMContext):
    async with state.proxy() as info:
        info['first_name'] = message.text
    await FSM_USER_REGISRER.next()
    await message.reply("User, Send me your last_name please")


async def load_last_name(message: types.Message,
                         state: FSMContext):
    async with state.proxy() as info:
        info['last_name'] = message.text
    await FSM_USER_REGISRER.next()
    await message.reply("Вы зарегистрировались")
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    await bot_db.user_insert(state)
    await state.finish()


def register_handler_user(dp: Dispatcher):
    dp.register_message_handler(is_user_register_command, commands=['register'])
    dp.register_message_handler(cancel_command, state='*', commands=['Отмена'])
    dp.message_handler(cancel_command, Text(equals='cancel', ignore_case=False), state='*')
    dp.register_message_handler(fsm_start, commands=['reg'], state=None)
    dp.register_message_handler(load_photo,
                                content_types=['photo'], state=FSM_USER_REGISRER.photo)
    dp.register_message_handler(load_id, state=FSM_USER_REGISRER.id)
    dp.register_message_handler(load_username, state=FSM_USER_REGISRER.username)
    dp.register_message_handler(load_first_name, state=FSM_USER_REGISRER.first_name)
    dp.register_message_handler(load_last_name, state=FSM_USER_REGISRER.last_name)
