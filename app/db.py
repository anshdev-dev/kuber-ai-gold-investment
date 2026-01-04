import sqlite3
import uuid
from datetime import datetime

DB_NAME = "kuber_ai.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            created_at TEXT
        )
    """)

    # Gold orders table (UUID-based)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_orders (
            order_id TEXT PRIMARY KEY,
            user_id TEXT,
            amount REAL,
            gold_grams REAL,
            status TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_user_if_not_exists(user_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user_id,)
    )

    if not cur.fetchone():
        cur.execute(
            """
            INSERT INTO users (user_id, created_at)
            VALUES (?, ?)
            """,
            (user_id, datetime.utcnow().isoformat())
        )

    conn.commit()
    conn.close()


def create_gold_order(user_id: str, amount: float):
    """
    Mock gold purchase logic.
    Assumption: 1 gram gold = ₹6000
    """

    gold_price_per_gram = 6000
    gold_grams = round(amount / gold_price_per_gram, 6)

    order_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO gold_orders
        (order_id, user_id, amount, gold_grams, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            order_id,
            user_id,
            amount,
            gold_grams,
            "SUCCESS",
            created_at
        )
    )

    conn.commit()
    conn.close()

    return order_id, gold_grams
