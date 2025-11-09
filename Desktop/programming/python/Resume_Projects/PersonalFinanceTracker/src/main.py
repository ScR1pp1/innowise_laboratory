from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
import logging

from starlette import status

from src.api import auth, transactions, analytics, users, goals
from src.database import async_session_factory, engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Personal Finance Tracker",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(users.router, prefix="/users", tags=["profile"])
app.include_router(goals.router, prefix="/goals", tags=["goals"])

@app.get("/db-connection-check")
async def check():
    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as e:
        return {
            "database": "error",
            "detail": str(e)
        }


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    logger.error(f"Request body {await request.body()}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": [
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"],
                } for error in exc.errors()
            ]
        },
    )