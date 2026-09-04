"""
SQLite Chat Persistence & SQLite Escrow / Transactions Module
"""

import sqlite3

DB_NAME = "krishisetu_auth.db"

def save_chat_message(user_id, session_id, role, content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("INSERT INTO chat_history (user_id, session_id, role, content) VALUES (?, ?, ?, ?)",
                   (user_id, session_id, role, content))
    conn.commit()
    conn.close()

def load_chat_history(user_id, session_id="default"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        SELECT role, content FROM chat_history 
        WHERE user_id = ? AND session_id = ? 
        ORDER BY timestamp ASC
    """, (user_id, session_id))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def init_transactions_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id TEXT,
            buyer_id INTEGER,
            farmer_id INTEGER,
            amount REAL,
            status TEXT,
            escrow_release_date DATETIME,
            quality_certification TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
