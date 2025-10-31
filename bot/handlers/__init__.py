from bot.handlers.admin import admin_handlers
from bot.handlers.common import common_handlers
from bot.handlers.owner import owner_handlers
from bot.handlers.survey_maker import survey_maker_handlers

def register_handlers(bot):
    admin_handlers.register_handlers(bot)
    common_handlers.register_handlers(bot)
    owner_handlers.register_handlers(bot)
    survey_maker_handlers.register_handlers(bot)
