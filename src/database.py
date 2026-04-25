import sqlite3
from pathlib import Path

DB_PATH = Path("tasklogger.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                started_at TEXT DEFAULT (datetime('now')),
                ended_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                timestamp TEXT,
                action_type TEXT,
                detail TEXT,
                x INTEGER,
                y INTEGER,
                screenshot_before TEXT,
                screenshot_after TEXT,
                label TEXT DEFAULT 'unlabeled',
                approved INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def create_session(name):
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO sessions (name) VALUES (?)", (name,))
        conn.commit()
        return cur.lastrowid

def insert_action(session_id, action):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO actions
            (session_id, timestamp, action_type, detail, x, y, screenshot_before, screenshot_after)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            action['timestamp'],
            action['action_type'],
            action.get('detail', ''),
            action.get('x', 0),
            action.get('y', 0),
            action.get('screenshot_before', ''),
            action.get('screenshot_after', '')
        ))
        conn.commit()

def get_actions(session_id=None, limit=200):
    with get_conn() as conn:
        if session_id:
            rows = conn.execute(
                "SELECT * FROM actions WHERE session_id=? ORDER BY id DESC LIMIT ?",
                (session_id, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM actions ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

def approve_action(action_id, label):
    with get_conn() as conn:
        conn.execute(
            "UPDATE actions SET approved=1, label=? WHERE id=?",
            (label, action_id)
        )
        conn.commit()

def get_sessions():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT s.*, COUNT(a.id) as action_count,
                   SUM(a.approved) as approved_count
            FROM sessions s
            LEFT JOIN actions a ON s.id = a.session_id
            GROUP BY s.id ORDER BY s.id DESC
        """).fetchall()
        return [dict(r) for r in rows]

def get_stats():
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM actions").fetchone()[0]
        approved = conn.execute("SELECT COUNT(*) FROM actions WHERE approved=1").fetchone()[0]
        sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        return {"total": total, "approved": approved, "sessions": sessions}
