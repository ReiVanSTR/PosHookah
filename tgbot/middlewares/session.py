import logging
from aiogram import types
from ..models.dataclasses import Session

from aiogram.dispatcher.middlewares import BaseMiddleware 

class SessionMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.message, data: dict):
        logging.info(f"Pre process message {data=}")
        data['session'] = Session(True)