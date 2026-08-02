from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class Expense:
    id: str
    title: str
    amount: float
    category: str
    date: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Expense:
        return cls(
            id=data["id"],
            title=data["title"],
            amount=float(data["amount"]),
            category=data["category"],
            date=data["date"],
        )
