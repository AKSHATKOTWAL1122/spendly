---
name: database-setup
description: Implementation plan for SQLite database layer and seeding
type: project
---

# Context
The goal is to implement the core database layer for Spendly, a personal expense tracker. This involves setting up the SQLite schema, connection management, and initial demo data seeding as specified in `.claude/specs/01-database-setup.md`. This is a foundational step that enables user registration, login, and expense management.

# Recommended Approach

## 1. Implementation of `database/db.py`
I will implement the database utility module with the following components:
- **Connection Management**: `get_db()` will establish a connection to `spendly.db`, set `row_factory = sqlite3.Row` for name-based column access, and enable foreign key constraints using `PRAGMA foreign_keys = ON`.
- **Schema Initialization**: `init_db()` will create the `users` and `expenses` tables using `CREATE TABLE IF NOT EXISTS`.
    - `users` table: `id` (PK), `name`, `email` (UNIQUE), `password_hash`, `created_at`.
    - `expenses` table: `id` (PK), `user_id` (FK), `amount` (REAL), `category`, `date`, `description`, `created_at`.
- **Data Seeding**: `seed_db()` will populate the database with initial demo data if the `users` table is empty.
    - One demo user with a password hashed via `werkzeug.security.generate_password_hash`.
    - 8 sample expenses across all required categories (*Food, Transport, Bills, Health, Entertainment, Shopping, Other*) for the current month.

## 2. Integration in `app.py`
I will update the application entry point to ensure the database is ready upon startup:
- Import `init_db` and `seed_db` from `database.db`.
- Execute these functions within `with app.app_context():` before the server starts.

# Critical Files
- `database/db.py`: Primary implementation of DB logic.
- `app.py`: Application startup logic.

# Verification Plan
- **Database Creation**: Verify that `spendly.db` is created in the project root after running `app.py`.
- **Schema Validation**: Use a SQLite client to confirm table structures and constraints (UNIQUE email, NOT NULL fields).
- **Seeding Check**: Verify the existence of the demo user and exactly 8 sample expenses linked to that user.
- **Idempotency**: Restart the application to ensure `seed_db()` does not insert duplicate records.
- **Integrity Check**: Test foreign key enforcement by attempting to insert an expense with a non-existent `user_id`.
