from db import (check_general_statistic,
                check_survey_makers,
                delete_survey)
def register_handlers(bot):
    @bot.message_handler(commands=["Посмотреть общую статистику"])
    def command_handler(message):
        statistic = check_general_statistic()
        message = ""
        number = 1
        for i in statistic:
            message += f"{number}). тг id:{i}\n"
            for j in statistic[i]:
                for k in j:
                    message += f"\tВопрос: {k[0]}\n"
                    message += f"\tОтвет: {k[1]}\n"
            number += 1
        bot.send_message(message.chat.id, message)
        
def register_handlers(bot):
    @bot.message_handler(commands=["Квешн-мейкеры"])
    def command_handler(message):
        survey_makers = check_survey_makers()
        message = "Список квешн-мейкеров:\n"
        for i in survey_makers:
            message += f"тг id: {i.tg_id}, роль: {i.role_id}\n"
        bot.send_message(message.chat.id, message)

def register_handlers(bot):
    @bot.message_handler(commands=["Удалить опрос"])
    def command_handler(message):
        
