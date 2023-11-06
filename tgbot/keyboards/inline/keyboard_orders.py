import logging
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from tgbot import keyboards
from ..callback_factory import order_callback, bill_callback, cancel_callback, menu_callback

def make_bill_callback_data(action="static", table="0"):
	return bill_callback.new(action, table)

def make_menu_callback_data(level, action):
	return order_callback.new(level, action)


def create_bills_keyboard(bills_list: list):
	current_level = 1

	keyboard = []

	for bill in bills_list:
		_text = f"""Stolik {bill.table_name} {bill.persons} osób."""
		_callback_data = make_bill_callback_data("open_bill", bill.table_name)
		keyboard.append([InlineKeyboardButton(text = _text, callback_data = _callback_data)])


	keyboard.append([InlineKeyboardButton(text = " << ", callback_data = make_bill_callback_data("cancel", "None"))])
	return InlineKeyboardMarkup(inline_keyboard = keyboard)

def show_bill(bill):
	keyboard = []

	if bill.orders:
		for order in bill.orders:
			_text = f"L{order.order_id} | {order.count_cart()} PLN"
			keyboard.append([InlineKeyboardButton(text = _text, callback_data = make_bill_callback_data("open_order", order.order_id))])

		cache_row = [
			InlineKeyboardButton(text = "+", callback_data = bill_callback.new("append", bill.table_name)),
			InlineKeyboardButton(text = " close ", callback_data = bill_callback.new("close", bill.table_name)),
		]

		keyboard.append(cache_row)
		keyboard.append([InlineKeyboardButton(text = " << ", callback_data = bill_callback.new("show_bills", "None"))])		
	else:
		keyboard.append([InlineKeyboardButton(text = "(Nothing)", callback_data = make_bill_callback_data("None", "None"))])

		cache_row = [
			InlineKeyboardButton(text = "+", callback_data = bill_callback.new("append", bill.table_name)),
			InlineKeyboardButton(text = " close ", callback_data = bill_callback.new("close", bill.table_name)),
		]

		keyboard.append(cache_row)
		keyboard.append([InlineKeyboardButton(text = " << ", callback_data = bill_callback.new("show_bills", "None"))])

	return InlineKeyboardMarkup(inline_keyboard = keyboard) 


def show_order(bill, order_id):
	keyboard = []
	_order = bill.get_order_by_id(order_id)

	logging.log(30, f"{_order=}")

	for item in _order.cart:
		keyboard.append([InlineKeyboardButton(text = f"{item.name}, {item.cost}", callback_data = bill_callback.new("None", "None"))])

	keyboard.append([InlineKeyboardButton(text = " << ", callback_data = bill_callback.new("open_bill", bill.table_name))])

	return InlineKeyboardMarkup(inline_keyboard = keyboard) 


def generate_item_keyboard(data: dict):
	pass

def menu_categories_keyboard(categories):

	keyboard = []

	for category in categories:
		keyboard.append([InlineKeyboardButton(text = category.name, callback_data = make_menu_callback_data(2, "open"))])

	keyboard.append([InlineKeyboardButton(text = " << ", callback_data = make_menu_callback_data("0", "back"))])

	return InlineKeyboardMarkup(inline_keyboard = keyboard)



