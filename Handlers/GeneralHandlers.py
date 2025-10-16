from main import *
import psycopg2

@bot.message_handler(commands=["start", "Start"])
def start_handler(message):
    with psycopg2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT Role_id FROM Users WHERE user_id = %s", (message.from_user.id))

        checkExists = cursor.fetchone()

    if checkExists:
        bot.send_message(message.chat_id, "Привет!\n\nЯ - бот-опросник, и с помощью меня ты можешь проходить различные опубликованные опросы)", reply_markup=make_menu_keyboard(f"{checkExists[0]}"))
        return None

    cursor.execute(f"INSERT Users (tg_user_id) VALUES (%s) ON CONFLICT (tg_user_id) DO NOTHING", (message.from_user.id,))

    bot.send_message(message.chat.id, "Привет!\n\nЯ - бот-опросник, и с помощью меня ты можешь проходить различные опубликованные опросы)", reply_markup=make_menu_keyboard(1))

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
