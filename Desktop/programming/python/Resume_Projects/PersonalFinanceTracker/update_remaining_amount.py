#!/usr/bin/env python3
import asyncio
from sqlalchemy import select, update
from src.database import async_session_factory, engine, Base
from src.models.goal import Goal


async def update_remaining_amount():
    async with async_session_factory() as session:
        result = await session.execute(select(Goal))
        goals = result.scalars().all()
        
        print(f"{len(goals)} update targets found")
        
        for goal in goals:
            remaining_amount = max(0, goal.target_amount - goal.current_amount)
            
            await session.execute(
                update(Goal)
                .where(Goal.id == goal.id)
                .values(remaining_amount=remaining_amount)
            )
            
            print(f"Target '{goal.name}': remaining_amount = {remaining_amount}")
        
        await session.commit()
        print("✅ All targets updated successfully!")


async def main():
    print("🔄 Updating remaining_amount field...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await update_remaining_amount()
    
    await engine.dispose()
    print("✅ Finish!")


if __name__ == "__main__":
    asyncio.run(main())
