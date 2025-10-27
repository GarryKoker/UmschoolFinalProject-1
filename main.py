from dotenv import load_dotenv

load_dotenv()

import os
import logging
from telebot import *
from db.db_adapter import *
from bot.handlers.__init__ import register_handlers
from bot.init_bot import create_bot

telebot.logger.setLevel(logging.INFO) #Outputs messages to console.

if __name__ == "__main__":
    create_tables_in_db()
    bot = create_bot(os.getenv("TG_TOKEN"))
    register_handlers(bot)
    bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))
    print("Bot is active!")
    bot.infinity_polling()
