from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import router, set_store
from src.storage import ExpenseStore

store = ExpenseStore()


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.load()
    set_store(store)
    yield


app = FastAPI(
    title="Smart Expense Tracker API",
    description=(
        "A RESTful API to manage personal expenses. Supports adding, viewing, "
        "filtering, aggregating, and deleting expenses."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {"status": "ok", "service": "Smart Expense Tracker API"}
