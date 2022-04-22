import asyncio
import aioschedule
from aiogram import types, Dispatcher
from config import bot
from decouple import config


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await bot.send_message(message.chat.id,
                           "got your id")


async def go_to_met_friends():
    await bot.send_message(chat_id=chat_id,
                           text="YES!\n"
                                "To day is friday!")
    photo = open('media/friday.jpg', 'rb')
    await bot.send_photo(chat_id=chat_id,
                         photo=photo)


async def scheduler():
    aioschedule.every().friday.at("00:01").do(go_to_met_friends)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_handler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id, lambda word: 'notify' in word.text)
