"""
DB validation test placeholder.
"""
import sqlite3
from pathlib import Path

import pytest

DB_PATH = Path(__file__).resolve().parents[2] / "app" / "data" / "bank.db"

pytestmark = pytest.mark.db


def test_tomer_admin_exists_in_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
    SELECT username, first_name, last_name, role, is_active
    FROM users
    WHERE username = ?
    """,
    ("tomer_admin",))

    user = cursor.fetchone()
    print(dict(user))

    assert user is not None
    assert user["username"] == "tomer_admin"
    assert user["first_name"] == "Tomer"
    assert user["last_name"] == "Gil-Or"
    assert user["role"] == "admin"
    assert user["is_active"] == 1

    connection.close()
