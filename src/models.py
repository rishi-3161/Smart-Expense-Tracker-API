"""Data models for the Expense Tracker."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Expense:
    """Represents a single expense record.

    Attributes:
        id: Unique identifier (UUID4 string).
        title: Short description of the expense.
        amount: Monetary amount (must be > 0).
        category: Expense category (e.g. "food", "transport").
        date: Date of the expense in YYYY-MM-DD format.
    """

    id: str
    title: str
    amount: float
    category: str
    date: str  # YYYY-MM-DD

    def to_dict(self) -> dict:
        """Serialize the expense to a plain dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Expense:
        """Deserialize an expense from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            amount=float(data["amount"]),
            category=data["category"],
            date=data["date"],
        )
