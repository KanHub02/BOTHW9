from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import admin_kb
from config import bot
from database import bot_db, psql_db


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
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    await bot_db.sql_insert(state)
    await state.finish()


async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_delete(call.data.replace("delete ", ""))
    await call.answer(text=f'{call.data.replace("delete ", "")} deleted',
                      show_alert=True)


async def complete_user_delete(call: types.CallbackQuery):
    await bot_db.sql_delete(call.data.replace("delete ", ""))
    await call.answer(text=f'{call.data.replace("delete ", "")} deleted',
                      show_alert=True)


async def delete_data(message: types.Message):
    selected_data = await bot_db.sql_casual_select()
    for result in selected_data:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=result[0],
            caption=f'Title: {result[1]}\n Description: {result[2]}',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f'delete: {result[1]}',
                    callback_data=f'delete {result[1]}'
                )
            )
        )


async def delete_user(message: types.Message):
    selected_data = await bot_db.user_casual_select()
    for show in selected_data:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=show[0],
            caption=f'telegram_acount_id {show[1]}\n'
                    f'username: {show[2]}\n'
                    f'first_name {show[3]}\n'
                    f'last_name: {show[4]}',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f'delete: {show[2]}',
                    callback_data=f'delete {show[2]}'
                )
            )
        )
async def add_bike(message: types.Message):
    photo = FSMADMIN.photo.set()
    await message.reply("Admin, Send me photo please")
    desc = message.from_user
    await message.reply("Admin, Send me description ")
    psql_db.cursor.execute(
        "INSERT INTO users (photo, decription) VALUES (%s, %s)",
        (photo, desc),
    )
    psql_db.db.commit()
    await message.reply("Registration successful")



async def registration(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    psql_db.cursor.execute(
        "INSERT INTO users (id, username, fullname) VALUES (%s, %s, %s)",
        (id, username, fullname),
    )
    psql_db.db.commit()
    await message.reply("Registration successful")
async def get_all_bikes(message: types.Message):
    all_bikes = psql_db.cursor.execute("SELECT * FROM bikes")
    result = psql_db.cursor.fetchall()

    for row in result:
        await message.reply(
            f"Photo: {row[0]}\n"
            f"Description: {row[1]}\n"
        )

async def get_all_users(message: types.Message):
    all_users = psql_db.cursor.execute("SELECT * FROM users")
    result = psql_db.cursor.fetchall()

    for row in result:
        await message.reply(
            f"ID: {row[0]}\n"
            f"Username: {row[1]}\n"
            f"Fullname: {row[2]}"
        )


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(is_admin_command, commands=['admin'])
    dp.register_message_handler(cancel_command, state='*', commands=['cancel'])
    dp.message_handler(cancel_command, Text(equals='cancel', ignore_case=False), state='*')
    dp.register_message_handler(fsm_start, commands=['upload'], state=None)
    dp.register_message_handler(load_photo,
                                content_types=['photo'], state=FSMADMIN.photo)
    dp.register_message_handler(load_title, state=FSMADMIN.title)
    dp.register_message_handler(load_description, state=FSMADMIN.description)
    dp.register_callback_query_handler(
        complete_delete,
        lambda call: call.data and call.data.startswith("delete "))
    dp.register_message_handler(delete_data, commands=['delete'])
    dp.register_callback_query_handler(
        complete_user_delete,
        lambda call: call.data and call.data.startswith("zxc"))
    dp.register_message_handler(delete_user, commands=['zxc'])
    dp.register_message_handler(registration, commands=['register'])
    dp.register_message_handler(get_all_users, commands=['get'])
    dp.register_message_handler(add_bike, commands=['addbike'])
    dp.register_message_handler(get_all_bikes, commands=['bikes'])