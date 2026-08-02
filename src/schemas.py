from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short description of the expense",
        json_schema_extra={"examples": ["Lunch at café"]},
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Monetary amount (must be greater than zero)",
        json_schema_extra={"examples": [12.50]},
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Expense category",
        json_schema_extra={"examples": ["food"]},
    )
    date: str = Field(
        ...,
        description="Date of the expense in YYYY-MM-DD format",
        json_schema_extra={"examples": ["2026-08-01"]},
    )

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date must be in YYYY-MM-DD format")
        return v

    @field_validator("category")
    @classmethod
    def normalize_category(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        return v.strip()


class ExpenseResponse(BaseModel):
    id: str
    title: str
    amount: float
    category: str
    date: str

    model_config = {"json_schema_extra": {
        "examples": [{
            "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "title": "Lunch at café",
            "amount": 12.50,
            "category": "food",
            "date": "2026-08-01",
        }]
    }}


class TotalResponse(BaseModel):
    total: float = Field(..., description="Sum of expense amounts")
    category: Optional[str] = Field(
        None, description="Category name, if filtered"
    )
    count: int = Field(..., description="Number of expenses included")


class MonthlySummaryItem(BaseModel):
    month: str = Field(..., description="Year-month string, e.g. '2026-08'")
    total: float = Field(..., description="Total expenses for this month")
    count: int = Field(..., description="Number of expenses in this month")


class MonthlySummaryResponse(BaseModel):
    summary: list[MonthlySummaryItem]
