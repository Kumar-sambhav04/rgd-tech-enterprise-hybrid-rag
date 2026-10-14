from sqlalchemy import text
import os

from app.database.connection import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("Database connection successful!")
        print(result.fetchone())

except Exception as e:
    print("Database connection failed:")
    print(e)


###Connection Code******import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

database_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(database_url,pool_pre_ping=True)