import json
import logging
from typing import List
from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from dataclasses import dataclass, field

from tgbot.misc.db import DB
from tgbot.misc.states import Navigation
from tgbot.models.dataclasses import Hookah
from tgbot.keyboards.callback_factory import category_callback, bill_callback

selector_callback = CallbackData("Selector","action", "data", sep = "|")

@dataclass
class Category():
    name: str
    contains: list = field(default_factory = list)


types = {
    "hookah":Hookah,
}

class InlineMenu:
    def __init__(
            self,
            db: DB,
    ) -> None:
        self.db = db
        self.categories = self.load_categories()
        self.cart = {}

    def load_categories(self):
        response = []

        categories = self.db.load_menu_cache()
        for category in categories:
            _cat = Category(**category)
            if _cat.contains:
                _buff = []
                for item in _cat.contains:
                    _item = types[item["type"]](**item)
                    _buff.append(_item)
                _cat.contains = _buff
            response.append(_cat)

        return response
    
    def create_menu_categories_keyboard(self):
        keyboard = []

        for category in self.categories:
            _text = f"{category.name}"
            _callback = category_callback.new("open_category", json.dumps({"current_category":category.name}))
            keyboard.append([InlineKeyboardButton(text = _text, callback_data = _callback)])
        
        keyboard.append([InlineKeyboardButton(text = "<<", callback_data = bill_callback.new("open_bill", "static"))])

        return InlineKeyboardMarkup(inline_keyboard = keyboard)
    
    def create_category_keyboard(self, category_name):
        _current_category = [category for category in self.categories if category.name == category_name][0]

        keyboard = []
        logging.log(30, _current_category)
        for item in _current_category.contains:
            _text = f"{item.name} | {item.cost}"
            _callback_data = selector_callback.new("pass", "pass")
            keyboard.append([InlineKeyboardButton(text = _text, callback_data = _callback_data)])
            
            cache_row = []
            _callback_data = selector_callback.new("add_item", json.dumps({"category":_current_category.name, "item":item.name}))
            cache_row.append(InlineKeyboardButton(text = "+", callback_data = _callback_data))

            _callback_data = selector_callback.new("pass", "pass")
            _text = self.cart.get(item.name) if item.name in self.cart else "0"
            cache_row.append(InlineKeyboardButton(text = _text, callback_data = _callback_data))

            _callback_data = selector_callback.new("remove_item", json.dumps({"category":_current_category.name, "item":item.name}))
            cache_row.append(InlineKeyboardButton(text = "-", callback_data = _callback_data))

            keyboard.append(cache_row)
            _callback_data = category_callback.new("open_menu_categories", "static")
            keyboard.append([InlineKeyboardButton(text = "<<", callback_data = _callback_data)])
        if not _current_category.contains:
            _callback_data = category_callback.new("open_menu_categories", "static")

            keyboard.append([InlineKeyboardButton(text = "<<", callback_data = _callback_data)])

        return InlineKeyboardMarkup(inline_keyboard = keyboard)
    
    async def select_from_category_process(self, call: CallbackQuery, callback_data: dict):
        logging.log(30, callback_data.values())
        action, data = callback_data.values()

    
    def register_selectors(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.select_from_category_process, selector_callback.filter(action = ["add_item", "remove_item"]), state = Navigation.bill_navigation)

