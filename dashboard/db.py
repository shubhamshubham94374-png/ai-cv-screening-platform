import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load the .env file from the project root (one level up from this dashboard folder)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def run_query(sql: str) -> pd.DataFrame:
    """Runs a raw SQL query and returns the result as a pandas DataFrame."""
    return pd.read_sql(sql, engine)