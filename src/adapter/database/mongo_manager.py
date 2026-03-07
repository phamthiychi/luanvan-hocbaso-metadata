from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.common.settings import settings

class MongoManager:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_DB_URI, server_api=ServerApi('1'))
        self.admin = self.client.admin

    def get_core_db(self):
        return self.client[settings.CORE_DB]

    def get_db(self, db_name: str):
        return self.client[db_name]

mongo_manager = MongoManager()