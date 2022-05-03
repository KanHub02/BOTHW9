from aiogram.utils import executor
from decouple import config
from handlers import callback, client, extra, cllback_choose1, callback_choose2, fsmadmin, fsadmin_register, \
    notification, upload_media
from config import bot, dp, URL
from database import bot_db
import asyncio


async def on_startup(_):
    await bot.set_webhook(URL)
    bot_db.sql_create()
    asyncio.create_task(notification.scheduler())
    print("Bot is online")


async def on_shutdown(dp):
    await bot.delete_webhook()


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
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=int(config("PORT", default=5000))
    )