from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_active_user
from src.dependencies import get_async_db
from src.models.user import User
from src.schemas.analytics import (
    FinancialSummary, NetWorthHistory, CashFlowAnalysis,
    FinancialHealth, AnalyticsResponse, AnalyticsRequest
)
from src.services.analytics_service import AnalyticsService
from src.services.financial_analytics import FinancialAnalyticsService


router = APIRouter()

@router.get("/period", response_model=AnalyticsResponse)
async def get_period_analytics(
    request: AnalyticsRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_financial_analytics(request, current_user.id)

@router.get("/summary", response_model=FinancialSummary)
async def get_financial_summary(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_financial_summary(current_user.id)

@router.get("/total-balance", response_model=Dict)
async def get_total_balance(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    analytics_service = FinancialAnalyticsService(db)
    return await analytics_service.get_total_balance(current_user.id)

@router.get("/net-worth-trend", response_model=NetWorthHistory)
async def get_net_worth_trend(
    days: int = Query(30, description="Period in days"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    analytics_service = FinancialAnalyticsService(db)
    return await analytics_service.get_net_worth_trend(current_user.id, days)

@router.get("/cash-flow", response_model=CashFlowAnalysis)
async def get_cash_flow_analysis(
    start_date: datetime = Query(..., description="Start date"),
    end_date: datetime = Query(..., description="End date"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    analytics_service = FinancialAnalyticsService(db)
    return await analytics_service.get_cash_flow_analysis(current_user.id, start_date, end_date)

@router.get("/financial-health", response_model=FinancialHealth)
async def get_financial_health(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    analytics_service = FinancialAnalyticsService(db)
    return await analytics_service.get_financial_health_score(current_user.id)