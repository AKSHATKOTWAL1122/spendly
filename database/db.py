import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = 'spendly.db'

def get_db():
    """
    Establishes a connection to the SQLite database.
    - Sets row_factory to sqlite3.Row for name-based column access.
    - Enables foreign key constraints.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    """
    Initializes the database schema.
    Creates users and expenses tables if they do not exist.
    """
    with get_db() as db:
        # Users Table
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Expenses Table
        db.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        db.commit()

def create_user(name, email, password):
    with get_db() as db:
        db.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, generate_password_hash(password))
        )
        db.commit()

def seed_db():
    """
    Seeds the database with initial demo data if it's empty.
    - Creates one demo user.
    - Creates 8 sample expenses across all required categories.
    """
    with get_db() as db:
        # Check if users table is already populated
        user_exists = db.execute('SELECT id FROM users LIMIT 1').fetchone()
        if user_exists:
            return

        # Create Demo User
        demo_user_data = (
            'Demo User',
            'demo@spendly.com',
            generate_password_hash('demo123')
        )
        cursor = db.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            demo_user_data
        )
        user_id = cursor.lastrowid

        # Sample Expenses (8 records covering all categories)
        expenses = [
            (user_id, 12.50, 'Food', '2026-04-01', 'Lunch at cafe'),
            (user_id, 45.00, 'Transport', '2026-04-02', 'Gas refill'),
            (user_id, 120.00, 'Bills', '2026-04-05', 'Internet bill'),
            (user_id, 30.00, 'Health', '2026-04-08', 'Pharmacy'),
            (user_id, 15.00, 'Entertainment', '2026-04-10', 'Cinema ticket'),
            (user_id, 60.00, 'Shopping', '2026-04-12', 'Clothes'),
            (user_id, 10.00, 'Other', '2026-04-15', 'Misc item'),
            (user_id, 25.00, 'Food', '2026-04-20', 'Grocery shopping'),
        ]

        db.executemany(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
            expenses
        )
        db.commit()
