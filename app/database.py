import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "bank.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def get_user_by_username(username: str):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, username, password, first_name, last_name, role, is_active
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        return cursor.fetchone()
    finally:
        connection.close()


def get_accounts_for_user(user_id: int):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT account_number, account_type, balance, currency
            FROM accounts
            WHERE user_id = ?
            ORDER BY id
            """,
            (user_id,),
        )
        return cursor.fetchall()
    finally:
        connection.close()
