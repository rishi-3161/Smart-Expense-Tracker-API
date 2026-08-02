# AI Usage Notes

During the development of the Smart Expense Tracker API, I used AI tools (Claude / ChatGPT) as an pair-programming assistant to speed up routine scaffolding, boilerplate generation, and initial test suite drafting. Below is a detailed breakdown of how AI was integrated, what I verified and refined, and what suggestions I intentionally rejected.

---

## 1. AI-Generated vs. Written by Me

### AI-Generated Parts (Generated under my direction & guidance)
* **Boilerplate & Scaffolding**: Initial directory layout (`src/` and `tests/` split) and generic project files.
* **Pydantic Schema Scaffolding (`src/schemas.py`)**: Drafted the basic `ExpenseCreate` and `ExpenseResponse` model definitions and initial field validators.
* **FastAPI Route Signatures (`src/routes.py`)**: Scaffolded standard HTTP endpoint handlers (`POST`, `GET`, `DELETE`) with OpenAPI metadata decorators.
* **Initial Test Cases (`tests/test_api.py`)**: Generated standard pytest test functions for typical HTTP status code checks (e.g. 201 Created, 200 OK, 404 Not Found).
* **Docker & CI Scaffolding**: Drafted the initial `Dockerfile`, `.dockerignore`, and GitHub Actions workflow template.

### Written / Architected by Me
* **Overall Architecture & Tech Stack Selection**: Selected Python with FastAPI for its speed and built-in OpenAPI support, and implemented an in-memory dictionary store paired with local JSON file persistence.
* **Thread-Safe Storage Layer (`src/storage.py`)**: Designed the `ExpenseStore` class using `threading.Lock` to ensure thread safety across concurrent API requests.
* **Data Normalization Strategy**: Established lowercase category normalization on input to ensure consistent filtering and aggregation regardless of user casing.
* **Search & Aggregation Logic**: Designed the monthly grouping algorithm (YYYY-MM parsing) and multi-field substring matching for the search endpoint.
* **Test Isolation Design**: Structured the `store` test fixture (`data_file=None`) to ensure unit tests run strictly in-memory without polluting or reading local JSON files.

---

## 2. What I Validated, Tested, and Modified

* **Input Validation Rules**:
  * *AI Output*: The initial AI schema accepted zero or negative expense amounts and allowed empty string titles/categories.
  * *My Fix*: Added strict Pydantic constraints (`amount: float = Field(..., gt=0)`) and `@field_validator` methods to ensure non-empty strings and valid `YYYY-MM-DD` date formatting.
* **Preventing Side-Effects in Tests**:
  * *AI Output*: The AI initially initialized a single shared `ExpenseStore` writing to `expenses.json` during test runs.
  * *My Fix*: Refactored `conftest.py` to inject an isolated, in-memory `ExpenseStore(data_file=None)` per test, preventing tests from modifying local disk data or interfering with each other.
* **Category Search & Filter Behavior**:
  * *AI Output*: Filtering relied on exact string matching, causing `"Food"` and `"food"` to be treated as separate categories.
  * *My Fix*: Normalized all stored categories to lowercase and implemented case-insensitive substring searching across both title and category fields.
* **Error Handling & Status Codes**:
  * *AI Output*: Deleting an expense returned a generic 200 response regardless of whether the ID existed.
  * *My Fix*: Updated the delete handler to return `204 No Content` on success and raise an explicit `404 Not Found` if the expense ID does not exist.
* **Test Coverage Verification**:
  * Manually expanded test coverage to 37 test cases, validating edge cases such as invalid date formats, zero/negative amounts, missing payload fields, case-insensitive searching, and double-deletion.

---

## 3. AI Suggestions I Decided NOT to Use (and Why)

* **SQLAlchemy + SQLite Database**:
  * *Reason*: The AI suggested setting up an ORM with SQLite. I decided against this because the assignment explicitly permits in-memory or local JSON storage. Keeping a lightweight JSON-backed store avoids unnecessary database overhead while keeping the codebase clean and easy to evaluate.
* **JWT Authentication Middleware**:
  * *Reason*: The AI recommended adding JWT token authentication and user login routes. I omitted this because authentication was not part of the requirements and would add unnecessary friction to automated review scripts.
* **Alembic Database Migrations**:
  * *Reason*: Suggested alongside SQLAlchemy, but completely redundant for a JSON/in-memory data store.
* **Docker Compose with Redis Caching**:
  * *Reason*: Over-engineered for a single-service REST API. A simple `Dockerfile` is far more appropriate for this scale.

---

## 4. Summary of Implemented Bonuses

1. **OpenAPI / Swagger Documentation**: Full interactive docs available at `/docs` and `/redoc`.
2. **Monthly Summary Endpoint**: `GET /expenses/summary/monthly` groups expenses by year-month (`YYYY-MM`).
3. **Search Expenses Endpoint**: `GET /expenses/search?q=keyword` enables keyword search over titles and categories.
4. **Docker & Container Deployment**: Containerized with a slim `Dockerfile`, `.dockerignore`, and GitHub Actions pipeline configured for GitHub Container Registry (GHCR) and Render deployment.
5. **GitHub Actions**: A complete CI/CD pipeline that automatically tests, builds, and pushes Docker images to GitHub Container Registry (GHCR) on every push to `main` or `development`, ensuring consistent deployment. It also triggers Render deployments automatically.
