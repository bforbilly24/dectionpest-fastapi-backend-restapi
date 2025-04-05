# app/config/test_db.py
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("DATABASE_URL")
print(f"Using URL: {url}")
engine = create_engine(url)
connection = engine.connect()
print("Connection successful!")
connection.close()