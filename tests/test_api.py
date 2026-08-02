from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


class TestCreateExpense:
    def test_create_expense_returns_201(self, client: TestClient, sample_expense: dict):
        resp = client.post("/expenses", json=sample_expense)
        assert resp.status_code == 201

    def test_create_expense_returns_id(self, client: TestClient, sample_expense: dict):
        data = client.post("/expenses", json=sample_expense).json()
        assert "id" in data
        assert isinstance(data["id"], str)
        assert len(data["id"]) > 0

    def test_create_expense_echoes_fields(self, client: TestClient, sample_expense: dict):
        data = client.post("/expenses", json=sample_expense).json()
        assert data["title"] == sample_expense["title"]
        assert data["amount"] == sample_expense["amount"]
        assert data["date"] == sample_expense["date"]
        assert data["category"] == sample_expense["category"].lower()

    def test_create_expense_normalizes_category(self, client: TestClient):
        payload = {
            "title": "Test",
            "amount": 10.0,
            "category": "  FOOD  ",
            "date": "2026-01-01",
        }
        data = client.post("/expenses", json=payload).json()
        assert data["category"] == "food"

    def test_create_multiple_expenses_get_unique_ids(
        self, client: TestClient, sample_expense: dict
    ):
        id1 = client.post("/expenses", json=sample_expense).json()["id"]
        id2 = client.post("/expenses", json=sample_expense).json()["id"]
        assert id1 != id2


class TestGetExpenses:
    def test_list_empty_returns_empty_list(self, client: TestClient):
        resp = client.get("/expenses")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_created_expenses(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses")
        assert resp.status_code == 200
        assert len(resp.json()) == len(multiple_expenses)

    def test_get_by_id_returns_correct_expense(
        self, client: TestClient, sample_expense: dict
    ):
        created = client.post("/expenses", json=sample_expense).json()
        resp = client.get(f"/expenses/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]
        assert resp.json()["title"] == sample_expense["title"]

    def test_get_by_id_not_found(self, client: TestClient):
        resp = client.get("/expenses/nonexistent-id")
        assert resp.status_code == 404


class TestDeleteExpense:
    def test_delete_existing_returns_204(
        self, client: TestClient, sample_expense: dict
    ):
        created = client.post("/expenses", json=sample_expense).json()
        resp = client.delete(f"/expenses/{created['id']}")
        assert resp.status_code == 204

    def test_delete_removes_expense(self, client: TestClient, sample_expense: dict):
        created = client.post("/expenses", json=sample_expense).json()
        client.delete(f"/expenses/{created['id']}")
        resp = client.get(f"/expenses/{created['id']}")
        assert resp.status_code == 404

    def test_delete_nonexistent_returns_404(self, client: TestClient):
        resp = client.delete("/expenses/no-such-id")
        assert resp.status_code == 404

    def test_double_delete_returns_404(self, client: TestClient, sample_expense: dict):
        created = client.post("/expenses", json=sample_expense).json()
        client.delete(f"/expenses/{created['id']}")
        resp = client.delete(f"/expenses/{created['id']}")
        assert resp.status_code == 404


class TestValidation:
    def test_missing_title_returns_422(self, client: TestClient):
        payload = {"amount": 10.0, "category": "food", "date": "2026-01-01"}
        resp = client.post("/expenses", json=payload)
        assert resp.status_code == 422

    def test_empty_title_returns_422(self, client: TestClient):
        payload = {"title": "", "amount": 10.0, "category": "food", "date": "2026-01-01"}
        resp = client.post("/expenses", json=payload)
        assert resp.status_code == 422

    def test_negative_amount_returns_422(self, client: TestClient):
        payload = {"title": "Bad", "amount": -5.0, "category": "food", "date": "2026-01-01"}
        resp = client.post("/expenses", json=payload)
        assert resp.status_code == 422

    def test_zero_amount_returns_422(self, client: TestClient):
        payload = {"title": "Free", "amount": 0, "category": "food", "date": "2026-01-01"}
        resp = client.post("/expenses", json=payload)
        assert resp.status_code == 422

    def test_invalid_date_format_returns_422(self, client: TestClient):
        payload = {"title": "Bad date", "amount": 10.0, "category": "food", "date": "01-08-2026"}
        resp = client.post("/expenses", json=payload)
        assert resp.status_code == 422

    def test_non_date_string_returns_422(self, client: TestClient):
        payload = {"title": "Bad", "amount": 10.0, "category": "food", "date": "not-a-date"}
        resp = client.post("/expenses", json=payload)
        assert resp.status_code == 422

    def test_missing_category_returns_422(self, client: TestClient):
        payload = {"title": "No cat", "amount": 10.0, "date": "2026-01-01"}
        resp = client.post("/expenses", json=payload)
        assert resp.status_code == 422

    def test_empty_category_returns_422(self, client: TestClient):
        payload = {"title": "No cat", "amount": 10.0, "category": "", "date": "2026-01-01"}
        resp = client.post("/expenses", json=payload)
        assert resp.status_code == 422


class TestFilterByCategory:
    def test_filter_returns_matching_expenses(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses", params={"category": "food"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3
        assert all(e["category"] == "food" for e in data)

    def test_filter_case_insensitive(
        self, client: TestClient, sample_expense: dict
    ):
        client.post("/expenses", json=sample_expense)
        resp = client.get("/expenses", params={"category": "FOOD"})
        assert len(resp.json()) == 1

    def test_filter_nonexistent_category_returns_empty(self, client: TestClient):
        resp = client.get("/expenses", params={"category": "nope"})
        assert resp.status_code == 200
        assert resp.json() == []


class TestTotals:
    def test_total_empty_store(self, client: TestClient):
        resp = client.get("/expenses/total")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0.0
        assert data["count"] == 0

    def test_total_all_expenses(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses/total")
        data = resp.json()
        expected_total = sum(e["amount"] for e in multiple_expenses)
        assert data["total"] == pytest.approx(expected_total)
        assert data["count"] == len(multiple_expenses)

    def test_total_by_category(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses/total/food")
        data = resp.json()
        food_total = sum(e["amount"] for e in multiple_expenses if e["category"] == "food")
        food_count = sum(1 for e in multiple_expenses if e["category"] == "food")
        assert data["total"] == pytest.approx(food_total)
        assert data["count"] == food_count
        assert data["category"] == "food"

    def test_total_by_nonexistent_category(self, client: TestClient):
        resp = client.get("/expenses/total/nope")
        data = resp.json()
        assert data["total"] == 0.0
        assert data["count"] == 0


class TestMonthlySummary:
    def test_monthly_summary_empty(self, client: TestClient):
        resp = client.get("/expenses/summary/monthly")
        assert resp.status_code == 200
        assert resp.json()["summary"] == []

    def test_monthly_summary_groups_correctly(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses/summary/monthly")
        data = resp.json()["summary"]

        months = {item["month"] for item in data}
        assert months == {"2026-08", "2026-07"}

        aug = next(item for item in data if item["month"] == "2026-08")
        assert aug["total"] == pytest.approx(56.25)
        assert aug["count"] == 3

        jul = next(item for item in data if item["month"] == "2026-07")
        assert jul["total"] == pytest.approx(60.30)
        assert jul["count"] == 2


class TestSearch:
    def test_search_by_title_keyword(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses/search", params={"q": "lunch"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["title"] == "Lunch"

    def test_search_by_category_keyword(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses/search", params={"q": "transport"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["category"] == "transport"

    def test_search_case_insensitive(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses/search", params={"q": "UBER"})
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_search_partial_match(
        self, client: TestClient, multiple_expenses: list[dict]
    ):
        for exp in multiple_expenses:
            client.post("/expenses", json=exp)
        resp = client.get("/expenses/search", params={"q": "er"})
        assert resp.status_code == 200
        titles = {e["title"] for e in resp.json()}
        assert "Uber ride" in titles
        assert "Dinner" in titles

    def test_search_no_results(self, client: TestClient, sample_expense: dict):
        client.post("/expenses", json=sample_expense)
        resp = client.get("/expenses/search", params={"q": "xyz123"})
        assert resp.status_code == 200
        assert resp.json() == []

    def test_search_missing_query_returns_422(self, client: TestClient):
        resp = client.get("/expenses/search")
        assert resp.status_code == 422


class TestHealthCheck:
    def test_root_returns_ok(self, client: TestClient):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
