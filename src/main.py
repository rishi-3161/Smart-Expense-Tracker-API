"""FastAPI application entry-point for the Smart Expense Tracker."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import router, set_store
from src.storage import ExpenseStore


# ---------------------------------------------------------------------------
# Application lifespan — load data on startup
# ---------------------------------------------------------------------------

store = ExpenseStore()  # uses default expenses.json


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load persisted data when the server starts."""
    store.load()
    set_store(store)
    yield


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Smart Expense Tracker API",
    description=(
        "A RESTful API to manage personal expenses. Supports adding, viewing, "
        "filtering, aggregating, and deleting expenses. Data is persisted to a "
        "local JSON file."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for local development convenience.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


# ---------------------------------------------------------------------------
# Root health-check
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"], summary="Health check")
def root():
    """Simple health-check endpoint."""
    return {"status": "ok", "service": "Smart Expense Tracker API"}
