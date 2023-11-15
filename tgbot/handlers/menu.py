import logging
from aiogram import Dispatcher
from typing import Union
from aiogram import types
import json
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from tgbot.keyboards.inline.keyboard_inline_menu import InlineMenu
from tgbot.misc.db import DB

from tgbot.models.dataclasses import Session
from tgbot.keyboards.callback_factory import category_callback

from ..misc.states import Navigation


_keyboard = InlineMenu(DB("localhost", 6379))

async def open_menu_categories(call: CallbackQuery, state: FSMContext, session: Session):
	
	await call.message.edit_text(text = "Menu/Categories",  reply_markup = _keyboard.create_menu_categories_keyboard())

async def open_category(call: CallbackQuery, state: FSMContext, session: Session):
	data = await state.get_data()
	
	await call.message.edit_text(text = "Menu/Categories",  reply_markup = _keyboard.create_category_keyboard(data.get("current_category")))

async def navigate_menu(call: CallbackQuery, callback_data: dict, state: FSMContext, session: Session):
	
	action = {
		"open_menu_categories":open_menu_categories,
		"open_category":open_category,
	}
	
	_current_action = callback_data.get("action")
	_current_function = action[_current_action] # type: ignore

	if not callback_data.get("data") == "static":
		_current_data = json.loads(callback_data.get("data"))

		async with state.proxy() as storage:
			# if _current_action == "open_order":
			# 	storage["order_id"] = _current_data
			# else:
			# 	storage["current_table"] = _current_data
			async with state.proxy() as storage:
				for key, value in _current_data.items():
					storage[key] = value
			logging.log(30, [storage, "menu.py"])
	
    
	await _current_function(call, state, session) #type:ignore


def register_menu(dp: Dispatcher):
	dp.register_callback_query_handler(navigate_menu, category_callback.filter(action=["open_menu_categories", "open_category"]),state = [Navigation.order_navigation, Navigation.bill_navigation])
	_keyboard.register_selectors(dp)