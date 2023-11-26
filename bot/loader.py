import os

from telebot import TeleBot

bot = TeleBot(os.environ.get('BOT_TOKEN'))
