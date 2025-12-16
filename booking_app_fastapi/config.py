import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHMS = 'HS256'
ACCESS_TOKEN=30
REFRESH_TOKEN=7


