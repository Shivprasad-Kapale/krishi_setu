"""
Database & Authentication Module using SQLite3
Manages user accounts, multi-persona registration, login, and sessions.
"""

import sqlite3
import hashlib

DB_NAME = "krishisetu_auth.db"

def init_auth_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            mobile TEXT,
            persona TEXT NOT NULL,
            district TEXT,
            state TEXT
        )
    """)
    # Check if mobile column exists, if not add it (migration for existing DB)
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    if "mobile" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN mobile TEXT")
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, full_name, mobile, persona, district, state):
    init_auth_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, full_name, mobile, persona, district, state)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, hash_password(password), full_name, mobile, persona, district, state))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def authenticate_user(username, password):
    init_auth_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, full_name, mobile, persona, district, state 
        FROM users WHERE username = ? AND password = ?
    """, (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "full_name": user[2],
            "mobile": user[3],
            "persona": user[4],
            "district": user[5],
            "state": user[6]
        }
    return None
