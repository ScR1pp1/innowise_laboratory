import asyncio
from sqlalchemy import text
from src.database import async_session_factory, engine


async def add_remaining_amount_column():
    async with async_session_factory() as session:
        try:
            await session.execute(
                text("ALTER TABLE goals ADD COLUMN remaining_amount FLOAT DEFAULT 0.0")
            )
            await session.commit()
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e):
                raise


async def update_existing_goals():
    async with async_session_factory() as session:
        try:
            await session.execute(
                text("""
                    UPDATE goals 
                    SET remaining_amount = GREATEST(0, target_amount - current_amount)
                    WHERE remaining_amount IS NULL OR remaining_amount = 0
                """)
            )
            await session.commit()
        except Exception as e:
            raise


async def main():
    try:
        await add_remaining_amount_column()
        await update_existing_goals()
    except Exception as e:
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

