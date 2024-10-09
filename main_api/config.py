import os
from dotenv import load_dotenv

load_dotenv()

REQUESTS_PER_MINUTE_LIMIT = os.getenv("REQUESTS_PER_MINUTE_LIMIT")
DB_URI = os.getenv("DB_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
BROKER_URI = os.getenv("BROKER_URI")



