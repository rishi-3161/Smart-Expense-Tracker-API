from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.routes import set_store
from src.storage import ExpenseStore


@pytest.fixture()
def store() -> ExpenseStore:
    return ExpenseStore(data_file=None)


@pytest.fixture()
def client(store: ExpenseStore) -> TestClient:
    set_store(store)
    return TestClient(app)


@pytest.fixture()
def sample_expense() -> dict:
    return {
        "title": "Lunch at café",
        "amount": 12.50,
        "category": "food",
        "date": "2026-08-01",
    }


@pytest.fixture()
def multiple_expenses() -> list[dict]:
    return [
        {"title": "Lunch", "amount": 12.50, "category": "food", "date": "2026-08-01"},
        {"title": "Dinner", "amount": 25.00, "category": "food", "date": "2026-08-02"},
        {"title": "Uber ride", "amount": 18.75, "category": "transport", "date": "2026-08-01"},
        {"title": "Movie ticket", "amount": 15.00, "category": "entertainment", "date": "2026-07-28"},
        {"title": "Groceries", "amount": 45.30, "category": "food", "date": "2026-07-15"},
    ]
