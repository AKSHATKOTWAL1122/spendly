# Spec: Login and Logout

## Overview
This feature implements session-based authentication for Spendly. A registered user submits their email and password on the `/login` page; the server verifies the credentials against the hashed password in the database, writes the user's `id` and `name` into the Flask session on success, and redirects to `/profile`. Failed attempts re-render the form with an inline error. The `/logout` route clears the session and redirects to the landing page. This step gates all future authenticated routes and makes the session available to templates via `g` or direct session access.

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, hashed passwords in the database)

## Routes
- `GET /login` — render the login form — public
- `POST /login` — verify credentials, set session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/` — logged-in (no hard guard yet, safe to call when logged out)

## Database changes
No new tables or columns. The existing `users` table (`id`, `name`, `email`, `password_hash`) covers all requirements.

A new DB helper must be added to `database/db.py`:
- `get_user_by_email(email)` — fetches a single row from `users` where `email = ?`. Returns a `sqlite3.Row` or `None` if not found.

## Templates
- **Modify:** `templates/login.html`
  - Change the form `action` to `url_for('login')` with `method="post"`
  - Add `name` attributes to inputs: `email`, `password`
  - Add a block to display an inline error message (e.g. "Invalid email or password.")
  - Keep all existing visual design
- **Modify:** `templates/base.html`
  - Add conditional nav links: show "Logout" when `session.get('user_id')` is set, show "Login" and "Register" when it is not

## Files to change
- `database/db.py` — add `get_user_by_email(email)`
- `app.py` — upgrade `login()` to handle POST; implement `logout()`; add `session` to Flask imports; import `get_user_by_email` and `check_password_hash` from `werkzeug.security`
- `templates/login.html` — fix form action, add error display
- `templates/base.html` — add session-aware nav links

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available via the existing `werkzeug` install.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — no f-strings in SQL
- Password verification with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `get_user_by_email()` must live in `database/db.py`, not in the route
- Server-side validation must check:
  1. Both fields are non-empty
  2. A user with that email exists
  3. `check_password_hash(user['password_hash'], password)` returns `True`
  4. Show the same generic error ("Invalid email or password.") for both "not found" and "wrong password" — do not reveal which failed
- On success: `session['user_id'] = user['id']`, `session['user_name'] = user['name']`, then `redirect(url_for('profile'))`
- On failure: re-render `login.html` with an error — do not redirect
- `logout()` must call `session.clear()` then `redirect(url_for('landing'))`
- Use `abort(405)` if an unsupported HTTP method reaches the login route

## Definition of done
- [ ] `python app.py` starts without errors on port 5001
- [ ] `GET /login` renders the form with no errors
- [ ] Submitting a valid email and password sets the session and redirects to `/profile` (stub page is acceptable)
- [ ] Submitting an unrecognised email renders the form with "Invalid email or password."
- [ ] Submitting a correct email with a wrong password renders the form with "Invalid email or password."
- [ ] Submitting with any blank field renders the form with a validation error
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] After logout, navigating to `/login` shows the form (no leftover session data)
- [ ] Nav bar shows "Login" / "Register" when logged out and "Logout" when logged in
- [ ] No JS frameworks used; `requirements.txt` unchanged
