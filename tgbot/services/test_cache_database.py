from redis import Redis
from dataclasses import dataclass, field

from ..models.dataclasses import Session, Order, Bill, Hookah, Item

@dataclass
class DatabaseConfig():
    host: str
    port: str

@dataclass
class DefaultSession():
    key_name: str
    worker_id: int
    order_id: int = 0
    bills = field(default_factory = list)




class ServiceDatabase():
    def  __init__(self, connector: DatabaseConfig) -> None:
        self.connector = Redis(host = connector.host, port = connector.port)

    
class CacheDatabase():
    def __init__(self, database: ServiceDatabase) -> None:
        self.database = database

    