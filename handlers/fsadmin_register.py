from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import register_kb
from config import bot


async def help_command(message: types.Message):
    await bot.send_message(message.chat.id, '           READ ME         \n'
                                            '-----FIRST YOU MUST CHOOSE ADMIN OR USER configuration------'
                                            '/register command, registration\n'
                                            '/start command start\n'
                                            '/user command connection to user configuration\n'
                                            '/admin command like a user but only for special users')


class FSMUSER(StatesGroup):
    id = State()
    username = State()
    first_name = State()
    last_name = State()
    photo = State()


async def is_user_command(message: types.Message):
    global USER_ID
    USER_ID = message.from_user.id
    await bot.send_message(message.from_user.id,
                           f"Yes, {message.from_user.username}"
                           "What do you need",
                           reply_markup=register_kb.button_admin_register)
    await message.delete()


async def cancel_command(message: types.Message,
                         state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return "State is None, Relax"
    await state.finish()
    await message.reply("Canceled Successfully")


async def id_user(message: types.Message,
                  state: FSMContext):
    id_user = message.from_user.id
    async with state.proxy() as data:
        data['id'] = id_user
    await message.reply(f'Your id is {id_user}')


async def fsm_start(message: types.Message):
    await FSMUSER.photo.set()
    await message.reply("Send me your photo please")


async def load_photo(message: types.Message,
                     state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMUSER.next()
    await message.reply("Create a Username:")


async def load_username(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMUSER.next()
    await message.reply("First name:")


async def load_first_name(message: types.Message,
                          state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await FSMUSER.next()
    await message.reply('Last name:')


async def load_last_name(message: types.Message,
                         state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(help_command, commands=['help1'])
    dp.register_message_handler(is_user_command, commands=['user'])
    dp.register_message_handler(cancel_command, state='*', commands=['canceluser'])
    dp.message_handler(cancel_command, Text(equals='cancel', ignore_case=False), state='*')
    dp.register_message_handler(fsm_start, commands=['register'], state=None)
    dp.register_message_handler(load_photo,
                                content_types=['photo'], state=FSMUSER.photo)
    dp.register_message_handler(load_username, state=FSMUSER.username)
    dp.register_message_handler(load_first_name, state=FSMUSER.first_name)
    dp.register_message_handler(load_last_name, state=FSMUSER.last_name)
    dp.register_message_handler(id_user, state=FSMUSER.id)
