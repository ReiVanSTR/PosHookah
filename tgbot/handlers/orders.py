import logging
import json

from aiogram import Dispatcher
from typing import Union
from aiogram import types

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from ..keyboards.inline.keyboard_orders import show_order, show_bill, menu_categories_keyboard, create_bills_keyboard
from ..keyboards.callback_factory import bill_callback, menu_callback

from ..misc.states import Navigation
from ..misc.other import parse_time

from ..models.dataclasses import Bill, Session, Order


async def show_bills(message: Union[types.Message, types.CallbackQuery], state: FSMContext, session: Session, *kwarg):
	session.update()
	_markup = create_bills_keyboard(session.get_all_bills(False))

	if isinstance(message, types.Message):
		await Navigation.bill_navigation.set()
		await message.answer("Rachunki", reply_markup = _markup)

	elif isinstance(message, types.CallbackQuery):
		call = message
		await call.message.edit_text("Rachunki", reply_markup = _markup)


async def open_bill(call: CallbackQuery, state: FSMContext, session: Session):
	await Navigation.bill_navigation.set()

	data = await state.get_data()
	_bill = session.get_bill(data["current_table"]) 

	_text = f"""{_bill.table_name} ({_bill.persons} os) | {_bill.count()} PLN """
	_markup = show_bill(_bill)

	await call.message.edit_text(text = _text, reply_markup = _markup)

async def open_order(call: CallbackQuery, state: FSMContext, session: Session):
	# async with state.proxy() as storage:
	# 	_current_table = storage["current_table"]
	# 	_bill = session.get_bill(_current_table)

	# 	_order_id = storage["order_id"]
	data = await state.get_data()
	_bill = session.get_bill(data["current_table"]) 
	_order_id = data["current_order"]

	logging.log(30, f"{_bill=}, {_order_id}")
	_order = _bill.get_order_by_id(_order_id)
	_text = f"L{_order_id} Date: {parse_time(_order.time)}"
	_markup = show_order(_order, _bill)
	await call.message.edit_text(text = _text, reply_markup = _markup)



async def cancel(call: CallbackQuery, state: FSMContext, *kwargs):
	await state.finish()
	await call.message.delete()

async def navigate_orders(call: CallbackQuery, callback_data: dict, state: FSMContext, session: Session):

	_action = {
		"cancel":cancel,
		"show_bills":show_bills,
		"open_bill":open_bill,
		"open_order":open_order,
	}

	# _current_level = callback_data.get("level")
	# table = callback_data.get("table") if callback_data.get("table") else " "
	_current_action = callback_data.get("action")
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
			logging.log(30, [storage, "orders.py"])
	
	_current_function = _action[_current_action] # type: ignore

	await _current_function(call, state, session ) #type:ignore










def register_orders(dp: Dispatcher):
	dp.register_message_handler(show_bills, Text("Rachunki"))
	# dp.register_callback_query_handler(open_order, order_callback.filter(action = "open_bill"))
	dp.register_callback_query_handler(navigate_orders, bill_callback.filter(action=["open_bill","show_bills","cancel","open_order"]), state = [Navigation.bill_navigation, Navigation.order_navigation])
