from db_adapter import (check_smth_on_exists,
                        add_user_to_db,
                        get_user_from_db,
                        check_own_statistic)
from db_adapter import Users

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
        for i in result:
            bot.send_message(message.chat.id, i)

def register_handlers(bot):
    @bot.message_handler(commands=["Прохождение опроса"])
    def command_handler(message):
        bot.send_message(message.chat.id, "123")
