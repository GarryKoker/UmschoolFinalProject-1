def register_handlers(bot):
    @bot.message_handler(commands=["start", "Start"])
    def start_handler(message):
        bot.send_message(message.chat.id, "Привет!\n\nЯ - бот-опросник, и с помощью меня ты можешь проходить различные опубликованные опросы)")

def register_handlers(bot):
    @bot.message_handler(commands=["Просмотр личной статистики"])
    def command_handler(message):
        bot.send_message(message.chat.id, "123")

def register_handlers(bot):
    @bot.message_handler(commands=["Прохождение опроса"])
    def command_handler(message):
        bot.send_message(message.chat.id, "123")
