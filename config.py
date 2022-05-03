from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
URL = 'https://botbykanat.herokuapp.com/'
URI = 'postgres://vpzvjzoewctujb:6af063e5dde94969f8bfd82738b7da20d94bfe7b434bff02595daa26e72fcb5f@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com:5432/d7dcutq1lq5cqv'
