import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres@localhost:5432/smartretail_x",
)

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    result = connection.execute(text("SELECT current_database(), version();"))
    database, version = result.fetchone()

    print("PostgreSQL connection successful!")
    print(f"Database: {database}")
    print(f"Version: {version}")