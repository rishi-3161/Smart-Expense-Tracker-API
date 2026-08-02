"""Utility helpers for the Expense Tracker."""

from __future__ import annotations

import uuid


def generate_id() -> str:
    """Return a new UUID4 string to use as an expense ID."""
    return str(uuid.uuid4())
