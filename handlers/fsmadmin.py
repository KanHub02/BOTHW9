from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import admin_kb
from config import bot


class FSMADMIN(StatesGroup):
    photo = State()
    title = State()
    description = State()


async def is_admin_command(message: types.Message):
    global ADMIN_ID
    ADMIN_ID = message.from_user.id
    await bot.send_message(message.from_user.id,
                           "Yes, Admin\n"
                           "What do you need",
                           reply_markup=admin_kb.button_admin)
    await message.delete()


async def cancel_command(message: types.Message,
                         state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        current_state = await state.get_state()
        if current_state is None:
            return "State is None, Relax"
        await state.finish()
        await message.reply("Canceled Successfully")


async def fsm_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await FSMADMIN.photo.set()
        await message.reply("Admin, Send me photo please")


async def load_photo(message: types.Message,
                     state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMADMIN.next()
    await message.reply("Admin, Send me title of photo")


async def load_title(message: types.Message,
                     state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await FSMADMIN.next()
    await message.reply("Admin, Send me description of photo")


async def load_description(message: types.Message,
                           state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(is_admin_command, commands=['admin'])
    dp.register_message_handler(cancel_command, state='*', commands=['cancel'])
    dp.message_handler(cancel_command, Text(equals='cancel', ignore_case=False), state='*')
    dp.register_message_handler(fsm_start, commands=['upload'], state=None)
    dp.register_message_handler(load_photo,
                                content_types=['photo'], state=FSMADMIN.photo)
    dp.register_message_handler(load_title, state=FSMADMIN.title)
    dp.register_message_handler(load_description, state=FSMADMIN.description)
