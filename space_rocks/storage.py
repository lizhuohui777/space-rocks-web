"""网页和桌面游戏共用一个 SQLite 文件。"""
import sqlite3
from contextlib import closing
from pathlib import Path

DATABASE = Path(__file__).resolve().parents[1] / "data" / "players.sqlite3"


def connect():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db():
    DATABASE.parent.mkdir(exist_ok=True)
    with closing(connect()) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY, player_id INTEGER NOT NULL REFERENCES players(id),
                outcome TEXT NOT NULL CHECK(outcome IN ('win', 'loss', 'quit')),
                played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)


def add_player(username, password_hash):
    with closing(connect()) as db, db:
        db.execute("INSERT INTO players(username, password_hash) VALUES (?, ?)",
                   (username, password_hash))


def find_player(username):
    with closing(connect()) as db:
        return db.execute("SELECT * FROM players WHERE username = ?", (username,)).fetchone()


def save_result(player_id, outcome):
    with closing(connect()) as db, db:
        db.execute("INSERT INTO results(player_id, outcome) VALUES (?, ?)", (player_id, outcome))


def recent_results(player_id):
    with closing(connect()) as db:
        rows = db.execute("SELECT outcome, played_at FROM results WHERE player_id = ? "
                          "ORDER BY id DESC LIMIT 10", (player_id,))
        return [dict(row) for row in rows]
