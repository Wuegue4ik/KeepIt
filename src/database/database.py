import os
import sys
import warnings
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

try:
    DB_LOGIN = os.environ["DB_LOGIN"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_NAME = os.environ["DB_NAME"]
except KeyError as e:
    warnings.warn(f"[Env Error] .env variable {e} not found")
    sys.exit(1)

class DB_Base(DeclarativeBase):
    pass