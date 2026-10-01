import sqlite3
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "career_copilot.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Analysis History table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target_role TEXT NOT NULL,
            filename TEXT,
            skills TEXT,
            new_skills TEXT,
            interview_questions TEXT,
            projects TEXT,
            score INTEGER DEFAULT 80,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()

    # Default demo user from video (sagar@microsoft.com)
    cursor.execute("SELECT * FROM users WHERE email = 'sagar@microsoft.com'")
    if not cursor.fetchone():
        demo_pwd = generate_password_hash("password123")
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            ("sagar@microsoft.com", demo_pwd)
        )
        conn.commit()
    conn.close()

def register_user(email, password):
    conn = get_db()
    cursor = conn.cursor()
    try:
        pwd_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email.strip().lower(), pwd_hash)
        )
        conn.commit()
        return True, "User registered successfully!"
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user["password_hash"], password):
        return dict(user)
    return None

def save_analysis(user_id, target_role, filename, skills, new_skills, interview_questions, projects, score=85):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (user_id, target_role, filename, skills, new_skills, interview_questions, projects, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        target_role,
        filename,
        json.dumps(skills),
        json.dumps(new_skills),
        json.dumps(interview_questions),
        json.dumps(projects),
        score
    ))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_user_history(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        item = dict(r)
        item["skills"] = json.loads(item["skills"]) if item["skills"] else []
        item["new_skills"] = json.loads(item["new_skills"]) if item["new_skills"] else []
        item["interview_questions"] = json.loads(item["interview_questions"]) if item["interview_questions"] else []
        item["projects"] = json.loads(item["projects"]) if item["projects"] else []
        result.append(item)
    return result

def get_history_by_id(history_id, user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history WHERE id = ? AND user_id = ?", (history_id, user_id))
    r = cursor.fetchone()
    conn.close()
    if r:
        item = dict(r)
        item["skills"] = json.loads(item["skills"]) if item["skills"] else []
        item["new_skills"] = json.loads(item["new_skills"]) if item["new_skills"] else []
        item["interview_questions"] = json.loads(item["interview_questions"]) if item["interview_questions"] else []
        item["projects"] = json.loads(item["projects"]) if item["projects"] else []
        return item
    return None
