# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from config import DATA_DIR

DB_PATH = DATA_DIR / "redemptions.db"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS redemptions (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                birth_date TEXT NOT NULL,
                chs INTEGER NOT NULL,
                redeemed_at TEXT NOT NULL
            )
            """
        )


def has_redeemed(telegram_id: int) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM redemptions WHERE telegram_id = ?",
            (telegram_id,),
        ).fetchone()
    return row is not None


def get_redemption(telegram_id: int) -> sqlite3.Row | None:
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM redemptions WHERE telegram_id = ?",
            (telegram_id,),
        ).fetchone()


def mark_redeemed(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    birth_date: str,
    chs: int,
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO redemptions
                (telegram_id, username, first_name, birth_date, chs, redeemed_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (telegram_id, username, first_name, birth_date, chs, now),
        )
