import logging
from re import S

from typing import Union
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from ..keyboards.inline.keyboard_orders import show_bill, menu_categories_keyboard, create_bills_keyboard
from ..keyboards.callback_factory import bill_callback, menu_callback

from ..misc.states import Navigation

from ..models.dataclasses import Bill, Session, Order


async def show_bills(message: Union[types.Message, types.CallbackQuery], state: FSMContext, session: Session, *kwarg):

	_markup = create_bills_keyboard(session.get_all_bills(False))

	if isinstance(message, types.Message):
		await Navigation.bill_navigation.set()
		await message.answer("Rachunki", reply_markup = _markup)

	elif isinstance(message, types.CallbackQuery):
		call = message
		await call.message.edit_text("Rachunki", reply_markup = _markup)


async def open_bill(call: CallbackQuery, state: FSMContext, session: Session):
	await Navigation.bill_navigation.set()

	async with state.proxy() as storage:
		_current_table = storage["current_table"]
		if not _current_table == "None":
			_bill = session.get_bill(_current_table)

	_markup = show_bill(_bill)

	await call.message.edit_text(text = _bill.table_name, reply_markup = _markup)

async def cancel(call: CallbackQuery, state: FSMContext, *kwargs):
	await state.finish()
	await call.message.delete()

async def navigate_orders(call: CallbackQuery, callback_data: dict, state: FSMContext, session: Session):

	_action = {
		"cancel":cancel,
		"show_bills":show_bills,
		"open_bill":open_bill,
		"3":open_menu_categories
	}

	# _current_level = callback_data.get("level")
	# table = callback_data.get("table") if callback_data.get("table") else " "
	_current_action = callback_data.get("action")
	_current_table = callback_data.get("current_table")

	async with state.proxy() as storage:
		storage["current_table"] = _current_table
	
	_current_function = _action[_current_action] # type: ignore

	await _current_function(call, state, session ) #type:ignore












async def open_menu_categories(call: CallbackQuery, state: FSMContext, *kwargs):
	await Navigation.order_navigation.set()
	async with state.proxy() as storage:
		categories = storage["Session"].menu.get_categories()
	await call.message.edit_text(text = "Menu/Categories",  reply_markup = menu_categories_keyboard(categories))

async def navigate_menu(call: CallbackQuery, callback_data: dict, state: FSMContext):
	
	_level = {
		"0":open_bill,
		"1":open_menu_categories
	}

	_current_level = callback_data.get("level")
	_current_function = _level[_current_level] # type: ignore
	table = callback_data.get("table") or "S5"
	await _current_function(call, state, table) #type:ignore

def register_orders(dp: Dispatcher):
	dp.register_message_handler(show_bills, Text("Rachunki"))
	# dp.register_callback_query_handler(open_order, order_callback.filter(action = "open_bill"))
	dp.register_callback_query_handler(navigate_orders, bill_callback.filter(action=["open_bill","show_bills","cancel"]), state = Navigation.bill_navigation)
	dp.register_callback_query_handler(navigate_menu, menu_callback.filter(action=["back"]), state = Navigation.order_navigation)