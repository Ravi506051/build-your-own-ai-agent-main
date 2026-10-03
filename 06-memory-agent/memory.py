"""SQLite-backed long-term memory store for the chat agent."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone


class MemoryStore:
    """Persist and retrieve user facts from a SQLite database."""

    def __init__(self, db_path: str = "memory.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def add(self, fact: str, category: str) -> None:
        """Add a new fact with category and timestamp."""
        fact = fact.strip()
        if not fact:
            return
        ts = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            "INSERT INTO memory (fact, category, created_at) VALUES (?, ?, ?)",
            (fact, category, ts),
        )
        self.conn.commit()

    def search(self, query: str, limit: int = 5) -> list[str]:
        """Search facts with simple LIKE matching on text."""
        query = query.strip()
        if not query:
            return []
        terms = [t for t in query.split() if len(t) > 2][:5] or [query]
        where = " OR ".join(["fact LIKE ?"] * len(terms))
        params = [f"%{term}%" for term in terms] + [limit]
        rows = self.conn.execute(
            f"SELECT fact FROM memory WHERE {where} ORDER BY id DESC LIMIT ?",
            params,
        ).fetchall()
        return [r[0] for r in rows]

    def get_all(self) -> list[str]:
        """Return all stored facts, newest first."""
        rows = self.conn.execute(
            "SELECT category, fact, created_at FROM memory ORDER BY id DESC"
        ).fetchall()
        return [f"[{cat}] {fact} ({ts})" for cat, fact, ts in rows]

    def clear(self) -> None:
        """Delete all stored memories."""
        self.conn.execute("DELETE FROM memory")
        self.conn.commit()
