from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, field_validator

from src.schemas.budget import BudgetAnalysis
from src.schemas.category import CategoryResponse
from src.schemas.transaction import TransactionResponse


class AnalyticsRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    account_ids: Optional[List[int]] = None
    tag_ids: Optional[List[int]] = None

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_date(cls, value):
        """Парсит даты из разных форматов"""
        if isinstance(value, str):
            formats = [
                '%Y-%m-%d',
                '%d.%m.%Y',
                '%d/%m/%Y',
                '%Y-%m-%dT%H:%M:%S',
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue

            raise ValueError(f"Invalid date format: {value}")
        return value

class CategoryAnalysis(BaseModel):
    category: CategoryResponse
    amount: float
    percentage: float

class AnalyticsResponse(BaseModel):
    period_start: datetime
    period_end: datetime
    total_income: float
    total_expenses: float
    balance: float
    currency: str
    by_tag: List[CategoryAnalysis]
    budget_status: List[BudgetAnalysis]
    top_expenses: List[TransactionResponse]

class FinancialSummary(BaseModel):
    total_balance: float
    total_income: float
    total_expenses: float
    net_worth: float
    account_balances: List[dict]
    upcoming_bills: List[TransactionResponse]

class NetWorthHistory(BaseModel):
    current_net_worth: float
    trend_data: List[Dict]
    period_days: int

class CashFlowAnalysis(BaseModel):
    total_income: float
    total_expense: float
    net_cash_flow: float
    income_by_category: Dict
    expense_by_category: Dict
    savings_rate: float

class FinancialHealth(BaseModel):
    score: int
    factors: List[str]
    emergency_fund_months: float
    savings_rate: float
    recommendations: List[str]


class ExpenseAnalysis:
    pass


class IncomeAnalysis:
    pass