# Spec: Registration

## Overview
This feature implements user account creation for Spendly. A visitor fills in their name, email, and password on the `/register` page. The server validates the input, hashes the password, inserts the new user into the `users` table, and redirects to `/login` on success. Inline error messages are shown for validation failures and duplicate emails without a page reload. On success the user is shown with a success message and then redirected to login page. This is the first step toward authenticated access to the expense tracker.

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`, `generate_password_hash` import)

## Routes
- `GET /register` — render the registration form — public
- `POST /register` — validate input, create user, redirect to login — public

## Database changes
No new tables or columns. The existing `users` table (`id`, `name`, `email UNIQUE NOT NULL`, `password_hash`, `created_at`) covers all requirements.
A new DB helper must be added to `database/db.py`:
- `create_user(name, email, password)` — hashes the password with `werkzeug`, inserts a row into `users`, returns the new user's `id`. Raises `sqlite3.IntegrityError` if the email is already taken (UNIQUE constraint).


## Templates
- **Modify**: `templates/register.html`
  - Change the form `action` to `url_for('register')` with `method="post"`
  - Add `name` attributes to all inputs: `name`, `email`, `password`, `confirm_password`
  - Add a block to display a flash error message (e.g. "Email already registered", "Passwords do not match")
  - Keep all existing visual design
#

## Files to change
- `database/db.py` — add `create_user(name, email, password)`
- `app.py` — upgrade `register()` to handle POST; add `request`, `redirect`, `url_for` to Flask imports; import `create_user` and `sqlite3`; add `app.secret_key`
- `templates/register.html` — fix hardcoded action URL

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` inside `db.py`, never in routes
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `create_user()` must live in `database/db.py`, not in the route
- Server-side validation must check:
  1. All fields are non-empty
  2. `password == confirm_password`
  3. Email is not already registered (catch `sqlite3.IntegrityError`)
- On any validation failure, re-render the form with a flashed error message — do not redirect
- On success redirect with `redirect(url_for('login'))` — do not render a template
- Use `abort(405)` if an unsupported HTTP method reaches the route
- All templates extend `base.html`
- `app.secret_key` must be set (needed for sessions in later steps)

## Definition of done
- [ ] `python app.py` starts without errors on port 5001
- [ ] `GET /register` renders the form with no errors
- [ ] Submitting valid name / email / password redirects to `/login`
- [ ] Submitting with an already-registered email renders the form with "An account with that email already exists."
- [ ] Submitting with a password shorter than 8 characters renders the form with "Password must be at least 8 characters."
- [ ] Submitting with any blank field renders the form with "All fields are required."
- [ ] New user is present in `spendly.db` with a hashed (not plaintext) password
- [ ] No JS frameworks used; `requirements.txt` unchanged
