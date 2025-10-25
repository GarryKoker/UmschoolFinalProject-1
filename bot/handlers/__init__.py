from bot.handlers.admin import admin_handlers
from bot.handlers.common import common_handlers
from bot.handlers.owner import owner_handlers
from bot.handlers.question_maker import question_handlers

def register_handlers(bot):
    admin_handlers.register_handlers(bot)
    common_handlers.register_handlers(bot)
    owner_handlers.register_handlers(bot)
    question_handlers.register_handlers(bot)
