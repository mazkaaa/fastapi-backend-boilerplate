# FastAPI Backend Boilerplate

A minimal FastAPI backend starter featuring an in-memory CRUD (no database yet), clean API docs (Swagger & ReDoc), and tests.

## Features

- Health check endpoint: `GET /health`
- In-memory CRUD for Items under `/api/items`
  - `GET /api/items/` — list items
  - `POST /api/items/` — create item
  - `GET /api/items/{id}` — get item by id
  - `PATCH /api/items/{id}` — partially update item
  - `DELETE /api/items/{id}` — delete item
- Swagger UI with examples: `GET /docs`
- ReDoc: `GET /redoc`

Note: Data is held in memory and resets on server restart.

## Requirements

- Python 3.10+

## Setup

```bash
# 1) Create & activate a virtualenv (recommended)
python -m venv .venv
source ./.venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure environment (optional)
cp .env.example .env
# Edit .env to your needs. Variables are read via pydantic-settings with the APP_ prefix.
# Example overrides:
#   APP_APP_NAME=My API
#   APP_ENVIRONMENT=production
#   APP_DEBUG=false
#   APP_HOST=127.0.0.1
```

## Run

```bash
uvicorn app.main:app --reload
```

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

## Example requests

```bash
# Health
curl -s http://127.0.0.1:8000/health

# List items (empty on start)
curl -s http://127.0.0.1:8000/api/items/

# Create item
curl -s -X POST http://127.0.0.1:8000/api/items/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "Sample", "description": "Test item"}'

# Get by id (replace 1 with the returned id)
curl -s http://127.0.0.1:8000/api/items/1

# Update description
curl -s -X PATCH http://127.0.0.1:8000/api/items/1 \
  -H 'Content-Type: application/json' \
  -d '{"description": "Updated"}'

# Delete
curl -i -X DELETE http://127.0.0.1:8000/api/items/1
```

## Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest -q
```

## Project layout

```text
app/
  core/settings.py  # Centralized settings using pydantic-settings (.env support)
  main.py            # FastAPI app, routes mounted, health endpoint
  routers/items.py   # Items router (CRUD endpoints)
  crud/items.py      # In-memory store and CRUD operations
  schemas/item.py    # Pydantic models for requests/responses

requirements.txt     # App dependencies
requirements-dev.txt # Dev/test-only dependencies
.env.example         # Example environment variables file
tests/
  test_items.py      # CRUD flow and health check tests
```

## Next steps

- Swap in-memory store for a real database (SQLModel/SQLAlchemy) and repositories
- Add middlewares (CORS, logging), error handling, and authentication
- Linting/formatting (ruff/black), pre-commit hooks
