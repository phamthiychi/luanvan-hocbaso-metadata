import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
    MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
    MONGO_DB_URI = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@hocbaso-data.wyldsrm.mongodb.net/?appName=HocBaSo-Data"

    CORE_DB = os.getenv("CORE_DB")
    # ANALYTICS_DB = os.getenv("ANALYTICS_DB")
    # AUDIT_DB = os.getenv("AUDIT_DB")

settings = Settings()