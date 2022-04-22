from aiogram.utils import executor

from handlers import callback, client, extra, cllback_choose1, callback_choose2, fsmadmin, fsadmin_register, \
    notification, upload_media
from config import bot, dp
from database import bot_db
import asyncio


async def on_startup(_):
    bot_db.sql_create()
    asyncio.create_task(notification.scheduler())
    print("Bot is online")


client.register_handlers_client(dp)
fsmadmin.register_handler_admin(dp)
fsadmin_register.register_handler_user(dp)
upload_media.register_handler_media(dp)

cllback_choose1.register_handler_callback(dp)
callback_choose2.register_handler_callback(dp)
callback.register_handlers_callback(dp)
notification.register_handler_notification(dp)
extra.register_handlers_other(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
