"""Shared pytest fixtures for the Expense Tracker test suite."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.routes import set_store
from src.storage import ExpenseStore


@pytest.fixture()
def store() -> ExpenseStore:
    """Provide a fresh, in-memory-only store for each test."""
    return ExpenseStore(data_file=None)


@pytest.fixture()
def client(store: ExpenseStore) -> TestClient:
    """Provide a TestClient wired to the fresh store."""
    set_store(store)
    return TestClient(app)


@pytest.fixture()
def sample_expense() -> dict:
    """Return a valid expense payload for reuse across tests."""
    return {
        "title": "Lunch at café",
        "amount": 12.50,
        "category": "food",
        "date": "2026-08-01",
    }


@pytest.fixture()
def multiple_expenses() -> list[dict]:
    """Return several expense payloads spanning different categories and months."""
    return [
        {"title": "Lunch", "amount": 12.50, "category": "food", "date": "2026-08-01"},
        {"title": "Dinner", "amount": 25.00, "category": "food", "date": "2026-08-02"},
        {"title": "Uber ride", "amount": 18.75, "category": "transport", "date": "2026-08-01"},
        {"title": "Movie ticket", "amount": 15.00, "category": "entertainment", "date": "2026-07-28"},
        {"title": "Groceries", "amount": 45.30, "category": "food", "date": "2026-07-15"},
    ]
