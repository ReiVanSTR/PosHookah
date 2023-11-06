import redis 

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

    def load_session_cache(self) -> list:
    	return self.connector.json().get("session", "$")[0]
	
    def load_menu_cache(self) -> list:
        return self.connector.json().get("default_menu", "$.categories")[0]

