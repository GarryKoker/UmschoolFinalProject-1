from db.db_adapter import (check_smth_on_exists,
                        add_user_to_db,
                        get_user_from_db,
                        check_own_statistic,
                        take_the_survey)
from db.db_adapter import Users
from telebot import *

def register_handlers(bot):
    @bot.message_handler(commands=["start", "Start"])
    def start_handler(message):
        bot.send_message(message.chat.id, "Привет!\n\nЯ - бот-опросник, и с помощью меня ты можешь проходить различные опубликованные опросы)")
        if check_smth_on_exists(Users, Users.id, message.from_user.id):
            return
        add_user_to_db(Users(Tg_user_id=message.from_user.id, Role_id=1))

def register_handlers(bot):
    @bot.message_handler(commands=["Просмотр личной статистики"])
    def command_handler(message):
        result = check_own_statistic(get_user_from_db(message.from_user.id))
        message = ""
        number = 1
        for i in result:
            message += f"{number}. {i.question.text}\n"
            number += 1
        bot.send_message(message.chat.id, message)

def register_handlers(bot):
    @bot.message_handler(commands=["Прохождение опроса"])
    def command_handler(message):
        result = take_the_survey(get_user_from_db(message.from_user.id))
        question_text = result[0].question_text
        inline_keyboard_markup = telebot.types.InlineKeyboardMarkup()
        inline_buttons = []
        for i in result[1]:
            inline_buttons.append(telebot.types.InlineKeyboardButton(f"{i.choice_text}"))
        
        for i in inline_buttons():
            inline_keyboard_markup.add(i)
        bot.send_message(f"{question_text}", reply_markup=inline_keyboard_markup)
