# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Spendly is a Flask-based expense tracker application. It is currently in an early development stage, with several core features (authentication, expense management) planned as part of a structured learning path.

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML (Jinja2 templates), CSS, JavaScript
- **Testing:** pytest, pytest-flask

## Architecture
- `app.py`: Main entry point and route definitions.
- `database/`: Database logic and connection handling (`db.py`).
- `templates/`: HTML templates for the frontend.
- `static/`: Static assets (CSS, JS).

## Common Development Tasks

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```
The app runs on port `5001` by default.

### Testing
```bash
# Run all tests
pytest
```

## Implementation Notes
- The project follows a step-by-step implementation guide for students.
- Database initialization and seeding logic should be located in `database/db.py`.
- Routes for logout, profile, and expense management are currently placeholders and need implementation.
