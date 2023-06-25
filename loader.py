import logging
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from config import *
from addons.database.DatabaseManager import DatabaseManager

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher()
db = DatabaseManager('addons/database/database.db')