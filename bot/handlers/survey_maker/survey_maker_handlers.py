from db.db_adapter import (check_maked_surveys)

def register_handlers(bot):
    @bot.message_handler(commands=["Посмотреть созданные опросы"])
    def command_handler(message):
        result = check_maked_surveys(message.from_user.id)
        if result:
            message = ""
            number = 1
            for i in result:
                message = f"{number}. {i.survey_text}"

def register_handlers(bot):
    @bot.message_handler(commands=["Создать опрос"])
    def command_handler(message):
        pass
