"""
database.py — SQLite storage layer for Finance Tracker v2
Handles all DB operations cleanly via the Database class.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional


class Transaction:
    """Represents a single financial transaction."""

    VALID_TYPES = ("income", "expense")
    CATEGORIES = {
        "income":  ["Salary", "Freelance", "Investment", "Gift", "Other"],
        "expense": ["Food", "Transport", "Rent", "Utilities",
                    "Shopping", "Health", "Education", "Entertainment", "Other"],
    }

    def __init__(
        self,
        amount: float,
        category: str,
        type_: str,
        description: str = "",
        date: Optional[str] = None,
        id_: Optional[int] = None,
    ):
        if type_ not in self.VALID_TYPES:
            raise ValueError(f"type_ must be one of {self.VALID_TYPES}")
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        self.id = id_
        self.amount = round(amount, 2)
        self.category = category
        self.type = type_
        self.description = description
        self.date = date or datetime.today().strftime("%Y-%m-%d")

    def __repr__(self):
        sign = "+" if self.type == "income" else "-"
        return f"[{self.date}] {sign}₹{self.amount:.2f} | {self.category} | {self.description}"


class Database:
    """Handles all SQLite operations for the finance tracker."""

    def __init__(self, db_path: str = "finance_tracker.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount      REAL    NOT NULL,
                    category    TEXT    NOT NULL,
                    type        TEXT    NOT NULL,
                    description TEXT,
                    date        TEXT    NOT NULL
                )
            """)
            conn.commit()

    def add(self, t: Transaction) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO transactions (amount, category, type, description, date) "
                "VALUES (?, ?, ?, ?, ?)",
                (t.amount, t.category, t.type, t.description, t.date),
            )
            conn.commit()
            return cur.lastrowid

    def get_all(self) -> List[Transaction]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM transactions ORDER BY date DESC"
            ).fetchall()
        return [self._row_to_transaction(r) for r in rows]

    def delete(self, transaction_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM transactions WHERE id = ?", (transaction_id,)
            )
            conn.commit()
            return cur.rowcount > 0

    def get_summary(self) -> dict:
        with self._connect() as conn:
            total_income = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='income'"
            ).fetchone()[0]
            total_expense = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='expense'"
            ).fetchone()[0]
            by_category = conn.execute(
                "SELECT category, type, SUM(amount) as total "
                "FROM transactions GROUP BY category, type"
            ).fetchall()
        return {
            "total_income":  round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "balance":       round(total_income - total_expense, 2),
            "by_category":   [dict(r) for r in by_category],
        }

    def get_monthly(self) -> list:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT strftime('%Y-%m', date) as month, type, SUM(amount) as total "
                "FROM transactions GROUP BY month, type ORDER BY month"
            ).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def _row_to_transaction(row) -> Transaction:
        return Transaction(
            id_=row["id"],
            amount=row["amount"],
            category=row["category"],
            type_=row["type"],
            description=row["description"],
            date=row["date"],
        )
