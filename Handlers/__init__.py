from Handlers.Admin import AdminHandlers
from Handlers.Common import CommonHandlers
from Handlers.Owner import OwnerHandlers
from Handlers.Question_maker import Question_makerHandlers
from Handlers import GeneralHandlers

def register_handlers(bot):
    AdminHandlers.register_handlers(bot)
    CommonHandlers.register_handlers(bot)
    OwnerHandlers.register_handlers(bot)
    Question_makerHandlers.register_handlers(bot)
    GeneralHandlers.register_handlers(bot)
