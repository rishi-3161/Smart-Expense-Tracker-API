"""API route definitions for the Expense Tracker."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from src.schemas import (
    ExpenseCreate,
    ExpenseResponse,
    MonthlySummaryResponse,
    TotalResponse,
)
from src.storage import ExpenseStore

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# The store instance is injected by main.py via the module-level variable.
store: ExpenseStore = ExpenseStore(data_file=None)


def set_store(s: ExpenseStore) -> None:
    """Replace the module-level store (called from main.py and tests)."""
    global store
    store = s


# ---------------------------------------------------------------------------
# CRUD endpoints
# ---------------------------------------------------------------------------


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new expense",
    description="Create a new expense entry. The server generates a unique ID.",
)
def create_expense(payload: ExpenseCreate) -> ExpenseResponse:
    expense = store.add(
        title=payload.title,
        amount=payload.amount,
        category=payload.category,
        date=payload.date,
    )
    return ExpenseResponse(**expense.to_dict())


@router.get(
    "",
    response_model=list[ExpenseResponse],
    summary="List expenses",
    description=(
        "Return all expenses.  Optionally filter by category using the "
        "`category` query parameter."
    ),
)
def list_expenses(
    category: str | None = Query(
        default=None,
        description="Filter by category (case-insensitive)",
    ),
) -> list[ExpenseResponse]:
    if category:
        expenses = store.filter_by_category(category)
    else:
        expenses = store.get_all()
    return [ExpenseResponse(**e.to_dict()) for e in expenses]


@router.get(
    "/total",
    response_model=TotalResponse,
    summary="Get total expenses",
    description="Calculate the sum of all expense amounts.",
)
def get_total() -> TotalResponse:
    total, count = store.total()
    return TotalResponse(total=total, count=count)


@router.get(
    "/total/{category}",
    response_model=TotalResponse,
    summary="Get total by category",
    description="Calculate the sum of expense amounts for a specific category.",
)
def get_total_by_category(category: str) -> TotalResponse:
    total, count = store.total_by_category(category)
    return TotalResponse(total=total, count=count, category=category.lower())


@router.get(
    "/summary/monthly",
    response_model=MonthlySummaryResponse,
    summary="Monthly expense summary",
    description="Return expenses grouped by month (YYYY-MM) with totals and counts.",
)
def monthly_summary() -> MonthlySummaryResponse:
    return MonthlySummaryResponse(summary=store.monthly_summary())


@router.get(
    "/search",
    response_model=list[ExpenseResponse],
    summary="Search expenses",
    description=(
        "Search expenses by keyword. Performs a case-insensitive substring "
        "match against the title and category fields."
    ),
)
def search_expenses(
    q: str = Query(
        ...,
        min_length=1,
        description="Search keyword to match against title or category",
    ),
) -> list[ExpenseResponse]:
    expenses = store.search(q)
    return [ExpenseResponse(**e.to_dict()) for e in expenses]


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Get a single expense",
    description="Retrieve an expense by its unique ID.",
)
def get_expense(expense_id: str) -> ExpenseResponse:
    expense = store.get_by_id(expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id '{expense_id}' not found",
        )
    return ExpenseResponse(**expense.to_dict())


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
    description="Remove an expense by its unique ID.",
)
def delete_expense(expense_id: str) -> None:
    deleted = store.delete(expense_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id '{expense_id}' not found",
        )
