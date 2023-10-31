import redis 

import redis.asyncio as asredis

rc = redis.Redis(host = "localhost", port = 6379, decode_responses=True)

def set_new_bill(data):
	# _current_order_id = rc.json().get("session", "$.order_id")[0]
	# data["order_id"] = _current_order_id
	# rc.json().set("session", "$.order_id", _current_order_id + 1)

	rc.json().arrappend("session", "$.rachunki", data)

def get_all_bills():
	return rc.json().get("session", "$.rachunki")[0]

def get_order(table):
	return rc.json().get("session", f"$.rachunki.[?(@.table=='{table}')]['orders']")[0]


def get_menu_categories():
	return rc.json().objkeys("defaul_menu", "$")[0]

def database_connector():
	return redis.Redis(host = "localhost", port = 6379, decode_responses=True)

class DB():
    def __init__(self, host, port):
        self.connector = redis.Redis(host = host, port = port, decode_responses=True)

    def load_cache(self):
    	return self.connector.json().get("session", "$")[0]

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state


        
    def get_conn(self):
        return self.connector

class AcDB():
    def __init__(self):
        self.client = asredis.from_url("redis://localhost:6379?decode_responses=True")

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state