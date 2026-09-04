"""
OTP Authentication & Quick Mobile Login Module
Allows farmers to log in instantly using their mobile number and 4-digit OTP.
"""

import sqlite3
import random

DB_NAME = "krishisetu_auth.db"

def get_user_by_mobile(mobile):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, full_name, mobile, persona, district, state 
        FROM users WHERE mobile = ?
    """, (mobile,))
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

def register_quick_farmer(mobile, full_name, district, state):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    username = f"farmer_{mobile}"
    password_hash = "quick_otp_user"
    persona = "🌾 शेतकरी / उत्पादक (Farmer)"
    
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password, full_name, mobile, persona, district, state)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, password_hash, full_name, mobile, persona, district, state))
        conn.commit()
    except Exception:
        pass
    conn.close()
    return get_user_by_mobile(mobile)
