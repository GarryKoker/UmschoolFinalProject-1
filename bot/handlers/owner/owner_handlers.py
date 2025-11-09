from db.db_adapter import (get_personal)

def register_handlers(bot):
    @bot.message_handler(commands=["Персонал"])
    def command_handler(message):
        users = get_personal()
        message_text = "Список персонала:\n"
        for user in users:
            message_text += f"тг id: {user.tg_user_id}, роль: {user.role_id}\n"
        bot.send_message(message.chat.id, message_text)
