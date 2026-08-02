# Smart Expense Tracker API

A RESTful API for managing personal expenses, built with **FastAPI** and **Python**. The application provides expense management capabilities with request validation, persistent local storage, interactive API documentation, automated testing, and containerized deployment.

## Features

* Create expenses with automatically generated UUIDs
* Retrieve all expenses
* Retrieve an expense by ID
* Filter expenses by category
* Search expenses by title or category (case-insensitive)
* Calculate total expenses (overall and by category)
* Delete expenses
* Generate monthly expense summaries
* Interactive OpenAPI documentation (Swagger UI & ReDoc)
* Docker support for containerized deployment

---

## Technology Stack

| Component        | Technology                      |
| ---------------- | ------------------------------- |
| Language         | Python 3.10+                    |
| Framework        | FastAPI                         |
| Validation       | Pydantic v2                     |
| Storage          | In-memory with JSON persistence |
| Testing          | Pytest, FastAPI TestClient      |
| Documentation    | OpenAPI 3.1, Swagger UI, ReDoc  |
| Containerization | Docker                          |

---

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   ├── storage.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
├── Dockerfile
├── .dockerignore
├── render.yaml
├── requirements.txt
├── pytest.ini
├── README.md
└── AI_NOTES.md
```

---

## Installation

Clone the repository and install the required dependencies.

```bash
git clone <repository-url>
cd smart-expense-tracker
python -m venv .venv
```

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Local Development

```bash
uvicorn src.main:app --reload
```

The application will be available at:

```
http://localhost:8000
```

---

### Docker

Build the Docker image/Pull from GHCR:

```bash
docker build -t smart-expense-tracker .
```

or

```bash
docker pull ghcr.io/rishi-3161/smart-expense-tracker-api:latest
```

Run the container:

```bash
docker run -p 8000:8000 smart-expense-tracker
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation         | URL             |
| --------------------- | --------------- |
| Swagger UI            | `/docs`         |
| ReDoc                 | `/redoc`        |
| OpenAPI Specification | `/openapi.json` |

---

## Running Tests

Execute the complete test suite:

```bash
pytest
```

or

```bash
python -m pytest -v
```

---

## API Endpoints

| Method | Endpoint                        | Description                             |
| ------ | ------------------------------- | --------------------------------------- |
| GET    | `/`                             | Health check                            |
| POST   | `/expenses`                     | Create a new expense                    |
| GET    | `/expenses`                     | Retrieve all expenses                   |
| GET    | `/expenses?category={category}` | Filter expenses by category             |
| GET    | `/expenses/search?q={keyword}`  | Search expenses                         |
| GET    | `/expenses/{id}`                | Retrieve an expense by ID               |
| DELETE | `/expenses/{id}`                | Delete an expense                       |
| GET    | `/expenses/total`               | Calculate total expenses                |
| GET    | `/expenses/total/{category}`    | Calculate total expenses for a category |
| GET    | `/expenses/summary/monthly`     | Retrieve monthly expense summary        |

---

## Example Requests

### Create an Expense

```bash
curl -X POST http://localhost:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Lunch",
        "amount": 12.50,
        "category": "Food",
        "date": "2026-08-01"
      }'
```

### Retrieve All Expenses

```bash
curl http://localhost:8000/expenses
```

### Filter by Category

```bash
curl "http://localhost:8000/expenses?category=Food"
```

### Search Expenses

```bash
curl "http://localhost:8000/expenses/search?q=lunch"
```

### Calculate Total Expenses

```bash
curl http://localhost:8000/expenses/total
```

### Retrieve Monthly Summary

```bash
curl http://localhost:8000/expenses/summary/monthly
```

### Delete an Expense

```bash
curl -X DELETE http://localhost:8000/expenses/{expense_id}
```

---

## Data Persistence

Expense records are maintained in memory during application execution and are automatically persisted to a local JSON file, ensuring data is retained across application restarts.

---

## Continuous Integration

The repository includes a GitHub Actions workflow that automatically:

* Installs project dependencies
* Executes the complete test suite
* Builds the Docker image
* Publishes the Docker image to GitHub Container Registry (GHCR) on eligible branch pushes

---

## License

This project is proprietary and is provided for evaluation purposes only.

© 2026 Rushyendra. All Rights Reserved.

Unauthorized copying, redistribution, or submission of this work as academic coursework is prohibited.
