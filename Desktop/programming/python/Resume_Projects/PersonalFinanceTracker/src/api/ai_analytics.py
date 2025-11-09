from typing import Dict

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_active_user
from src.dependencies import get_async_db
from src.models.user import User
from src.services.advanced_ai_categorization import AdvancedAICategorizationService
from src.services.advanced_ai_prediction import AdvancedAIPredictionService
from src.services.behavioral_ai_advisor import BehavioralAIAdvisorService

router = APIRouter()

@router.post("/auto-categorize")
async def advanced_auto_categorize_transaction(
    description: str,
    amount: float,
    current_user: User = Depends(get_current_active_user)
):
    categorization_service = AdvancedAICategorizationService()
    category = await categorization_service.categorize_transaction(description, amount)
    return {"category": category}

@router.get("/advanced-predictions")
async def get_advanced_predictions(
    months: int = Query(6, description="Months to predict"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    prediction_service = AdvancedAIPredictionService(db)
    return await prediction_service.predict_financial_future(current_user.id, months)

@router.get("/behavioral-advice")
async def get_behavioral_advice(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    advisor_service = BehavioralAIAdvisorService(db)
    return await advisor_service.generate_personalized_advice(current_user.id)
