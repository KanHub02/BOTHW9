from aiogram.utils import executor

from handlers import callback, client, extra, cllback_choose1, callback_choose2, fsmadmin, fsadmin_register
from config import bot, dp
from database import bot_db


async def on_startup(_):
    bot_db.sql_create()
    print("Bot is online")


client.register_handlers_client(dp)
fsmadmin.register_handler_admin(dp)
fsadmin_register.register_handler_user(dp)

cllback_choose1.register_handler_callback(dp)
callback_choose2.register_handler_callback(dp)
callback.register_handlers_callback(dp)
extra.register_handlers_other(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
