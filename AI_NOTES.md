# AI Usage Notes

## Which parts were AI-generated vs. written by me

### AI-generated (with my direction and review)
- **Initial project structure** — I described the desired layout (`src/`, `tests/`, models/routes/storage split) and the AI scaffolded the files.
- **Pydantic schemas** (`schemas.py`) — the AI generated the `ExpenseCreate`, `ExpenseResponse`, `TotalResponse`, and `MonthlySummaryResponse` models with field validators.
- **CRUD endpoint scaffolding** (`routes.py`) — the AI produced the initial FastAPI router with endpoint signatures, status codes, and OpenAPI metadata.
- **Test cases** (`test_api.py`) — the AI generated the bulk of the pytest test suite based on the endpoint specification I provided.
- **Dockerfile & .dockerignore** — the AI generated the Docker container configuration for FastAPI/uvicorn deployment.
- **README template** — the AI drafted the README structure, which I reviewed and edited.

### Written / designed by me
- **Overall architecture decisions** — choosing FastAPI, in-memory + JSON persistence, the separation into models/schemas/storage/routes/utils.
- **API design** — the endpoint paths, HTTP methods, status codes, query parameters for category filtering and keyword search.
- **Storage design** — the `ExpenseStore` class structure, thread-safety approach (`threading.Lock`), and the decision to use UUID4 for IDs.
- **Category normalization & Search logic** — deciding to lowercase all categories on input for consistent querying, and substring matching across titles and categories for search.

## What I validated, tested, or changed

- **Verified all endpoints** manually using FastAPI's Swagger UI after starting the server.
- **Input validation**: confirmed that negative/zero amounts, empty titles, empty categories, and malformed dates are all rejected with 422 responses.
- **Corrected JSON persistence**: ensured the store doesn't write to disk during tests (by passing `data_file=None`), preventing test pollution.
- **Improved error handling**: verified that deleting a non-existent expense returns 404, and that double-deletes also return 404.
- **Reviewed test assertions**: verified that the test suite covers CRUD, validation, filtering, search, totals, monthly summary, and edge cases (37 tests total).
- **Category normalization & Search**: tested keyword search with case-insensitivity, partial matches, category matching, and empty results.

## Optional bonuses implemented

1. **OpenAPI/Swagger documentation** — FastAPI's built-in support provides interactive API docs at `/docs` (Swagger UI) and `/redoc` (ReDoc). I added endpoint summaries, descriptions, and example values to improve discoverability.
2. **Monthly summary endpoint** — `GET /expenses/summary/monthly` returns expenses grouped by year-month with totals and counts.
3. **Search expenses endpoint** — `GET /expenses/search?q=keyword` allows searching expenses by matching title or category.
4. **Docker support & Deployment** — Added production-ready `Dockerfile` and `.dockerignore` to containerize the application, plus a GitHub Actions pipeline (`ci.yml`) that automatically builds and pushes the image to **GitHub Container Registry (GHCR)** (`ghcr.io`) and registers a **GitHub Deployment environment**.

## AI suggestions I decided not to use

- **SQLite / SQLAlchemy storage** — suggested by the AI, but the assignment explicitly allows in-memory or JSON storage. JSON keeps the implementation simpler and the codebase smaller, which is appropriate for this scope.
- **JWT authentication middleware** — suggested for securing endpoints, but omitted because authentication is outside the assignment scope and would add unnecessary complexity.
- **Alembic migrations** — suggested alongside SQLAlchemy, but irrelevant since we're not using a relational database.
- **Docker Compose with Redis caching** — over-engineered for a single-service, in-memory expense tracker.