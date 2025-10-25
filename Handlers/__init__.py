from handlers.admin import AdminHandlers
from handlers.common import CommonHandlers
from handlers.owner import OwnerHandlers
from handlers.question_maker import Question_makerHandlers
from handlers import GeneralHandlers

def register_handlers(bot):
    AdminHandlers.register_handlers(bot)
    CommonHandlers.register_handlers(bot)
    OwnerHandlers.register_handlers(bot)
    Question_makerHandlers.register_handlers(bot)
    GeneralHandlers.register_handlers(bot)
