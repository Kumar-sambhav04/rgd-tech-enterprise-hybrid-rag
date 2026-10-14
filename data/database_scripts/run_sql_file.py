import sys
from pathlib import Path

from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()


database_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_MASTER_USER')}:"
    f"{os.getenv('POSTGRES_MASTER_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


def run_sql_file(file_path: Path):
    sql = file_path.read_text(encoding="utf-8")

    with engine.raw_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)

            if cursor.description:
                rows = cursor.fetchall()

                column_names = [
                column.name for column in cursor.description]

                print("\n" + " | ".join(column_names))
                print("-" * 70)

                for row in rows:
                    print(" | ".join(str(value) for value in row))

            

        connection.commit()

    print(f"Executed successfully: {file_path.name}")


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python data/database_scripts/run_sql_file.py <sql_filename>"
        )

    script_dir = Path(__file__).resolve().parent
    sql_file = script_dir / sys.argv[1]

    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    run_sql_file(sql_file)


if __name__ == "__main__":
    main()

## python data/database_scripts/run_sql_file.py chunk_registry_update.sql
## this file is to execute one sql file by ( this file name followed by the sql file name )