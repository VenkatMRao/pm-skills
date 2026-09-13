#!/usr/bin/env python3
"""Build a small SQLite sample database for trying nl-data-query without a real warehouse."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "sample.db"


def build():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            plan TEXT,
            signup_date TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL,
            order_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """
    )

    customers = [
        (1, "Aria Chen", "pro", "2026-01-05"),
        (2, "Ben Torres", "free", "2026-01-12"),
        (3, "Casey Lin", "pro", "2026-02-01"),
        (4, "Devon Osei", "enterprise", "2026-02-14"),
        (5, "Elena Petrova", "free", "2026-03-02"),
    ]
    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", customers)

    orders = [
        (1, 1, 49.0, "2026-02-01"),
        (2, 1, 49.0, "2026-03-01"),
        (3, 3, 49.0, "2026-02-10"),
        (4, 4, 499.0, "2026-02-20"),
        (5, 4, 499.0, "2026-03-20"),
        (6, 2, 0.0, "2026-01-15"),
    ]
    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)

    conn.commit()
    conn.close()
    print(f"Built sample database at {DB_PATH}")


if __name__ == "__main__":
    build()
