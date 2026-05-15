import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bank.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
SEED_PATH = BASE_DIR / "seed.sql"


def load_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_database() -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()
        cursor.executescript(load_sql(SCHEMA_PATH))
        cursor.executescript(load_sql(SEED_PATH))
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    build_database()
