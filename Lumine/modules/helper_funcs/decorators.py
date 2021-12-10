from Lumine.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.ext.filters import BaseFilter
from Lumine import dispatcher as d, log
from typing import Optional, Union, List


# Ported From Kigyo (@Kigyorobot) // https://github.com/AnimeKaizoku/EnterpriseALRobot
# By @AruotoxD (github.com/aruoto)


class KensurTelegramHandler:
    def __init__(self, d):
        self._dispatcher = d

    def callbackquery(self, pattern: str = None, run_async: bool = True):
        def _callbackquery(func):
            self._dispatcher.add_handler(CallbackQueryHandler(pattern=pattern, callback=func, run_async=run_async))
            log.debug(f'[KENSURCALLBACK] Loaded callbackquery handler with pattern {pattern} for function {func.__name__}')
            return func
        return _callbackquery

    def inlinequery(self, pattern: Optional[str] = None, run_async: bool = True, pass_user_data: bool = True, pass_chat_data: bool = True, chat_types: List[str] = None):
        def _inlinequery(func):
            self._dispatcher.add_handler(InlineQueryHandler(pattern=pattern, callback=func, run_async=run_async, pass_user_data=pass_user_data, pass_chat_data=pass_chat_data, chat_types=chat_types))
            log.debug(f'[KENSURINLINE] Loaded inlinequery handler with pattern {pattern} for function {func.__name__} | PASSES USER DATA: {pass_user_data} | PASSES CHAT DATA: {pass_chat_data} | CHAT TYPES: {chat_types}')
            return func
        return _inlinequery

kensurcallback = KensurTelegramHandler(d).callbackquery
kensurinline = KensurTelegramHandler(d).inlinequery
