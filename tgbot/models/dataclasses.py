from dataclasses import dataclass, field, is_dataclass
from ..misc.db import DB
from ..misc.other import real_time


@dataclass
class Item():
    name: str
    cost: int

    def prefix(self):
        return {"name": self.name, "cost": self.cost}

@dataclass
class Tabacco():
    brand: str
    name: str
    used: float = 0

@dataclass
class Hookah(Item):
    notes: str
    strong: int
    used_tabacco: list = field(default_factory = list)
    type: str = "hookah"
    

@dataclass
class Category():
    name: str
    items: list = field(default_factory = list)
    is_avalible: bool = True

    def _append_item(self, item):
        if item.get("used_tabacco"):
            _buff = []
            for tabacco in item.get("used_tabacco"):
                _buff.append(Tabacco(**tabacco))
            
            item["used_tabacco"] = _buff
            self.items.append(Hookah(**item))

    

@dataclass
class DefaultMenu():
     
    def __init__(self, cache):
        self.cache = cache
        self.categories = self.create_categories(self.cache)

    def create_categories(self, list_category: list) -> list:
        _buff = []
        for category in list_category:
            _buffer_category = Category(category.get("name"))

            if category.get("items"):
                for item in category.get("items"):
                    _buffer_category._append_item(item)
            
            _buff.append(_buffer_category)

        return _buff

    def get_categories(self) -> list:
        return self.categories
        

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

        return _cost


@dataclass
class Bill():
    table_name: str
    persons: int
    orders: list = field(default_factory = list)
    time:dict = field(default_factory = lambda: real_time())

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
    
    def count(self) -> int:
        to_paymant = 0
        if self.orders:
            for order in self.orders:
                to_paymant += order.count_cart()

        return to_paymant
    
    def get_order_by_id(self, order_id):
        return [order for order in self.orders if order.order_id == int(order_id)][0]


@dataclass
class Session():
    _db = DB("localhost", 6379)

    def __init__(self, update: bool):
        if update:
            self.update()

    def update(self):
        self.cache = self._db.load_session_cache()

        self.worker = self.cache.get("worker")
        self.order_id = self.cache.get("order_id")
        self.bills = []
        self.menu = DefaultMenu(self._db.load_menu_cache())

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




