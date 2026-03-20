import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
    MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
    POSTGRES_DB_PASSWORD = os.getenv("POSTGRES_DB_PASSWORD")
    MONGO_DB_URI = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@hocbaso-data.wyldsrm.mongodb.net/?appName=HocBaSo-Data"
    POSTGRES_DB_URI = f"postgresql://postgres.ypitqepyiqihlvwanqfs:{POSTGRES_DB_PASSWORD}@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

    CORE_MONGO_DB = os.getenv("CORE_MONGO_DB")
    # ANALYTICS_DB = os.getenv("ANALYTICS_DB")
    # AUDIT_DB = os.getenv("AUDIT_DB")

settings = Settings()