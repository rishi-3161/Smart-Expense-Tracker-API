# AI Usage Notes

## AI-generated

- Initial FastAPI project structure
- CRUD endpoint scaffolding
- Example pytest test cases
- README template

## What I validated

- Verified all endpoints manually using FastAPI Swagger UI.
- Added input validation for positive amounts.
- Corrected JSON persistence to prevent duplicate IDs.
- Improved error handling for missing expenses.
- Wrote additional tests to verify filtering and total calculations.

## Optional bonus implemented:
- OpenAPI/Swagger documentation using FastAPI's built-in support.
- Added endpoint summaries, descriptions, and example request models to improve API discoverability.

## Suggestions I did not use

- SQLite storage was suggested but not used because the assignment explicitly allows in-memory or JSON storage, and JSON keeps the implementation simpler.
- JWT authentication was suggested but omitted because it was outside the assignment scope.