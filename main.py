import telebot
from telebot import storage
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "Start"])
def start_handler(message):
    # with psycopg2.connect(os.getenv("DATABASE_URL")) as connection:
    #     print("Connecting")
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT Role_id FROM Users WHERE user_id = %s", (message.from_user.id))

    #     checkExists = cursor.fetchone()

    # if checkExists:
    #     bot.send_message(message.chat_id, "Привет!\n\nЯ - бот-опросник, и с помощью меня ты можешь проходить различные опубликованные опросы)", reply_markup=make_menu_keyboard(f"{checkExists[0]}"))
    #     return None

    #     cursor.execute(f"INSERT Users (tg_user_id) VALUES (%s) ON CONFLICT (tg_user_id) DO NOTHING", (message.from_user.id,))

        bot.send_message(message.chat.id, "Привет!\n\nЯ - бот-опросник, и с помощью меня ты можешь проходить различные опубликованные опросы)", reply_markup=make_menu_keyboard(1))

def check_role(tg_id: int) -> str:
    pass

def make_menu_keyboard(role_id: int) -> telebot.types.ReplyKeyboardMarkup:
    if role_id == 1:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
            telebot.types.KeyboardButton("Просмотр личной статистики"),
            telebot.types.KeyboardButton("Прохождение опроса"))

    elif role_id == 2:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
            telebot.types.KeyboardButton("Просмотр личной статистики"),
            telebot.types.KeyboardButton("Прохождение опроса"),
            telebot.types.KeyboardButton("Посмотреть созданные опросы"),
            telebot.types.KeyboardButton("Создать опрос"))

    elif role_id == 3:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
            telebot.types.KeyboardButton("Просмотр личной статистики"),
            telebot.types.KeyboardButton("Прохождение опроса"),
            telebot.types.KeyboardButton("Посмотреть созданные опросы"),
            telebot.types.KeyboardButton("Создать опрос"),
            telebot.types.KeyboardButton("Посмотреть общую статистику"),
            telebot.types.KeyboardButton("Квешн-мейкеры"),
            telebot.types.KeyboardButton("Удалить опрос"))

    elif role_id == 4:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
            telebot.types.KeyboardButton("Просмотр личной статистики"),
            telebot.types.KeyboardButton("Прохождение опроса"),
            telebot.types.KeyboardButton("Просмотреть созданные опросы"),
            telebot.types.KeyboardButton("Создать опрос"),
            telebot.types.KeyboardButton("Просмотреть общую статистику"),
            telebot.types.KeyboardButton("Персонал"),
            telebot.types.KeyboardButton("Удалить опрос"))

@bot.message_handler(commands=["Просмотр личной статистики"])
def command_handler(message):
    with psycopg2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT question_text, choice_text FROM Questions, Choices WHERE (SELECT id FROM Users == SELECT user_id FROM UserStatistic) and (SELECT id FROM Questions == SELECT question_id FROM UsersStatistic)")
        
        results = cursor.fetchall()
    
    message_to_user = "Ваша статистика:\n\n"
    
    for i in results:
        message_to_user += f"Вопрос: {i[0]}, ответ: {i[1]}\n"
    
    bot.send_message(message.chat.id, message_to_user)

@bot.message_handler(commands=["Прохождение опроса"])
def command_handler(message):
    with psycopg2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute("Из таблицы Questions взять question_text при условии что в таблице User_statistic в столбце question_id нету id вопроса из таблицы Questions для столбца user_id который является внешним ключём для таблицы Users столбца id")
        
        Question = cursor.fetchone()[0]
        
        cursor.execute("Из таблицы Choices выбрать все choice_text которые попадают под условие: в таблице Question_Choice есть строки, где Question_id совпадает с ")
        

bot.infinity_polling()
