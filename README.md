# Smart Expense Tracker API

A RESTful API to manage personal expenses, built with **Python** and **FastAPI**.

## Features

- **Add** an expense (auto-generated UUID, title, amount, category, date)
- **View** all expenses
- **View** a single expense by ID
- **Filter** expenses by category
- **Search** expenses by keyword (bonus) — case-insensitive substring match on title and category
- **Calculate totals** — overall and by category
- **Delete** an expense
- **Monthly summary** (bonus) — expenses grouped by month (YYYY-MM)
- **OpenAPI / Swagger docs** (bonus) — interactive API documentation
- **Docker support** (bonus) — Containerized deployment with Docker & Dockerignore

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Validation | Pydantic v2 |
| Storage | In-memory + local JSON file |
| Testing | pytest + FastAPI TestClient |
| Docs | OpenAPI 3.1 (auto-generated) |
| Container | Docker |

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

### Option 1: Local Development

```bash
uvicorn src.main:app --reload
```

The server starts at **http://localhost:8000**.

### Option 2: Docker Container

Build the Docker image:

```bash
docker build -t smart-expense-tracker .
```

Run the container:

```bash
docker run -p 8000:8000 smart-expense-tracker
```

### Option 3: Deploy to Render

This repository includes a `render.yaml` Blueprint file for automatic deployment on Render:

1. Push this repository to GitHub.
2. Go to [Render Dashboard](https://dashboard.render.com/) -> **New +** -> **Blueprint**.
3. Connect your GitHub repository. Render automatically builds the Dockerfile and deploys your Web Service!

## API Documentation

After starting the server:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Running Tests

```bash
pytest
```

or using python module execution:

```bash
python -m pytest -v
```

## API Endpoints

| Method   | Endpoint                    | Description                          |
|----------|-----------------------------|--------------------------------------|
| `GET`    | `/`                         | Health check                         |
| `POST`   | `/expenses`                 | Add a new expense                    |
| `GET`    | `/expenses`                 | List all expenses                    |
| `GET`    | `/expenses?category=food`   | Filter expenses by category          |
| `GET`    | `/expenses/search?q=lunch`  | Search expenses by keyword (bonus)   |
| `GET`    | `/expenses/{id}`            | Get a single expense                 |
| `DELETE` | `/expenses/{id}`            | Delete an expense                    |
| `GET`    | `/expenses/total`           | Get total of all expenses            |
| `GET`    | `/expenses/total/{category}`| Get total for a specific category    |
| `GET`    | `/expenses/summary/monthly` | Monthly expense summary (bonus)      |

## Example Usage

### Add an expense

```bash
curl -X POST http://localhost:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Lunch", "amount": 12.50, "category": "food", "date": "2026-08-01"}'
```

### List all expenses

```bash
curl http://localhost:8000/expenses
```

### Filter by category

```bash
curl "http://localhost:8000/expenses?category=food"
```

### Search expenses

```bash
curl "http://localhost:8000/expenses/search?q=lunch"
```

### Get total expenses

```bash
curl http://localhost:8000/expenses/total
```

### Get monthly summary

```bash
curl http://localhost:8000/expenses/summary/monthly
```

### Delete an expense

```bash
curl -X DELETE http://localhost:8000/expenses/{id}
```

## Project Structure

```
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions CI workflow
├── README.md
├── AI_NOTES.md
├── requirements.txt
├── pytest.ini
├── render.yaml
├── Dockerfile
├── .dockerignore
├── src/
│   ├── __init__.py
│   ├── main.py         # FastAPI app entry point
│   ├── models.py       # Expense data model
│   ├── routes.py       # API endpoint definitions
│   ├── schemas.py      # Pydantic request/response schemas
│   ├── storage.py      # In-memory store with JSON persistence
│   └── utils.py        # Helper utilities
└── tests/
    ├── __init__.py
    ├── conftest.py     # Shared test fixtures
    └── test_api.py     # API test suite
```