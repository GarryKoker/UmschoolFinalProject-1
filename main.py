import telebot
from telebot import storage
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
