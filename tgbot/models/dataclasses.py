import logging
from dataclasses import dataclass, field, is_dataclass
from typing import List
import redis
from ..misc.db import DB
from ..misc.other import real_time


@dataclass
class Item():
    name: str
    cost: int

    def prefix(self):
        return {"name": self.name, "cost": self.cost}

@dataclass
class Hookah(Item):
    notes: str
    strong: int


@dataclass
class Order():
    order_id: int
    cart: list = field(default_factory = list)
    time: dict = field(default_factory = real_time())

    def update_cart(self):
        if self.cart:
            _buff = []
            for item in self.cart:
                if not is_dataclass(item):
                    _buff.append(Item(**item))
            self.cart = _buff

    def cart_append(self, item: Item):
        self.cart.append(item)

    def count_cart(self):
        _cost = 0
        for item in self.cart:
            _cost += item.cost

        return str(_cost)


@dataclass
class Bill():
    table_name: str
    persons: int
    orders: list = field(default_factory = list)
    time:dict = field(default_factory = real_time())

    def __repr__(self):
        return self.table_name

    def prefix(self):
        return {"table_name":self.table_name, "persons":self.persons}   

    def update_orders(self):
        if self.orders:
            _buff = []
            for order in self.orders:
                _order = Order(**order)
                _order.update_cart()
                _buff.append(_order)
            self.orders = _buff

    def append_order(self, order: Order):
        self.orders.append(order)

    def get_orders(self):
        return self.orders


@dataclass
class Session():
    _db = DB("localhost", 6379)

    def update(self):
        self.cache = self._db.load_cache()

        self.worker = self.cache.get("worker")
        self.order_id = self.cache.get("order_id")
        self.bills = []

        if self.cache.get("rachunki"):
            for bill in self.cache.get("rachunki"):
                _buff = Bill(**bill)
                _buff.update_orders()
                self.append_bill(_buff)

    def append_bill(self, bill: Bill):
        if is_dataclass(bill):
            self.bills.append(bill)

    def get_bill(self, table_name):
        self.update()

        if any(bill for bill in self.bills if bill.table_name == table_name):
            return [bill for bill in self.bills if bill.table_name == table_name][0]
        return

    def get_all_bills(self, parsed: bool):
        if parsed:
            resp = []
            for bill in self.bills:
                resp.append(bill.prefix())
            return resp
        return self.bills

    def get_bill_orders(self, table_name):
        pass





