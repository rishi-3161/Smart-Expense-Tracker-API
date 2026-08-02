from __future__ import annotations

import json
import threading
from collections import defaultdict
from pathlib import Path
from typing import Optional

from src.models import Expense
from src.utils import generate_id

_DEFAULT_DATA_FILE = Path("expenses.json")


class ExpenseStore:
    def __init__(self, data_file: Optional[Path] = _DEFAULT_DATA_FILE) -> None:
        self._expenses: dict[str, Expense] = {}
        self._lock = threading.Lock()
        self._data_file = data_file

    def load(self) -> None:
        if self._data_file is None or not self._data_file.exists():
            return
        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
                raw: list[dict] = json.load(f)
            with self._lock:
                self._expenses = {
                    item["id"]: Expense.from_dict(item) for item in raw
                }
        except (json.JSONDecodeError, KeyError):
            self._expenses = {}

    def _save(self) -> None:
        if self._data_file is None:
            return
        data = [exp.to_dict() for exp in self._expenses.values()]
        with open(self._data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, title: str, amount: float, category: str, date: str) -> Expense:
        expense = Expense(
            id=generate_id(),
            title=title,
            amount=amount,
            category=category,
            date=date,
        )
        with self._lock:
            self._expenses[expense.id] = expense
            self._save()
        return expense

    def get_all(self) -> list[Expense]:
        with self._lock:
            return sorted(
                self._expenses.values(),
                key=lambda e: (e.date, e.title),
                reverse=True,
            )

    def get_by_id(self, expense_id: str) -> Optional[Expense]:
        with self._lock:
            return self._expenses.get(expense_id)

    def delete(self, expense_id: str) -> bool:
        with self._lock:
            if expense_id in self._expenses:
                del self._expenses[expense_id]
                self._save()
                return True
            return False

    def filter_by_category(self, category: str) -> list[Expense]:
        cat_lower = category.strip().lower()
        with self._lock:
            return sorted(
                [e for e in self._expenses.values() if e.category == cat_lower],
                key=lambda e: (e.date, e.title),
                reverse=True,
            )

    def total(self) -> tuple[float, int]:
        with self._lock:
            amounts = [e.amount for e in self._expenses.values()]
            return (round(sum(amounts), 2), len(amounts))

    def total_by_category(self, category: str) -> tuple[float, int]:
        cat_lower = category.strip().lower()
        with self._lock:
            amounts = [
                e.amount
                for e in self._expenses.values()
                if e.category == cat_lower
            ]
            return (round(sum(amounts), 2), len(amounts))

    def monthly_summary(self) -> list[dict]:
        with self._lock:
            buckets: dict[str, list[float]] = defaultdict(list)
            for e in self._expenses.values():
                month_key = e.date[:7]
                buckets[month_key].append(e.amount)

        result = []
        for month_key in sorted(buckets.keys(), reverse=True):
            amounts = buckets[month_key]
            result.append({
                "month": month_key,
                "total": round(sum(amounts), 2),
                "count": len(amounts),
            })
        return result

    def search(self, query: str) -> list[Expense]:
        q = query.strip().lower()
        if not q:
            return self.get_all()
        with self._lock:
            return sorted(
                [
                    e
                    for e in self._expenses.values()
                    if q in e.title.lower() or q in e.category.lower()
                ],
                key=lambda e: (e.date, e.title),
                reverse=True,
            )

    def clear(self) -> None:
        with self._lock:
            self._expenses.clear()
            self._save()
