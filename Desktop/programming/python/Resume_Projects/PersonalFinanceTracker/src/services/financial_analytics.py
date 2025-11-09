# src/services/financial_analytics.py
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Account, Transaction, Goal
from src.models.main import CurrencyChoose, TransactionType
from src.schemas.analytics import (
    FinancialSummary, NetWorthHistory, CashFlowAnalysis, FinancialHealth,
)


class FinancialAnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_total_balance(self, user_id: int) -> Dict[str, Any]:
        """Расчет общего баланса по всем счетам"""
        result = await self.db.execute(
            select(Account).where(
                Account.owner_id == user_id,
                Account.is_active == True
            )
        )
        accounts = result.scalars().all()

        total_balance = sum(account.balance for account in accounts)

        balance_by_type = {}
        for account in accounts:
            account_type_str = account.type.value if hasattr(account.type, 'value') else str(account.type)
            if account_type_str not in balance_by_type:
                balance_by_type[account_type_str] = 0
            balance_by_type[account_type_str] += account.balance

        return {
            "total_balance": float(total_balance),
            "balance_by_account_type": balance_by_type,
            "account_count": len(accounts),
            "currency": "BYN"
        }

    async def get_net_worth_trend(self, user_id: int, days: int = 30) -> NetWorthHistory:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        current_balance = await self.get_total_balance(user_id)

        transactions_stmt = select(Transaction).where(
            Transaction.owner_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date,
            Transaction.is_deleted == False
        )
        result = await self.db.execute(transactions_stmt)
        transactions = result.scalars().all()

        daily_data = {}
        for transaction in transactions:
            date_key = transaction.date.date()
            if date_key not in daily_data:
                daily_data[date_key] = {"income": 0, "expense": 0}

            if transaction.type == TransactionType.INCOME:
                daily_data[date_key]["income"] += transaction.amount
            else:
                daily_data[date_key]["expense"] += transaction.amount

        net_worth_data = []
        running_balance = current_balance["total_balance"]

        dates = sorted(daily_data.keys(), reverse=True)
        for date in dates:
            daily_net = daily_data[date]["income"] - daily_data[date]["expense"]
            running_balance -= daily_net
            net_worth_data.append({
                "date": date,
                "net_worth": running_balance,
                "daily_income": daily_data[date]["income"],
                "daily_expense": daily_data[date]["expense"]
            })

        return NetWorthHistory(
            current_net_worth=current_balance["total_balance"],
            trend_data=sorted(net_worth_data, key=lambda x: x["date"]),
            period_days=days
        )

    async def get_cash_flow_analysis(self, user_id: int, start_date: datetime, end_date: datetime) -> CashFlowAnalysis:
        income_stmt = select(
            Transaction.category_id,
            func.sum(Transaction.amount).label('total')
        ).where(
            Transaction.owner_id == user_id,
            Transaction.type == TransactionType.INCOME,
            Transaction.date >= start_date,
            Transaction.date <= end_date,
            Transaction.is_deleted == False
        ).group_by(Transaction.category_id)

        income_result = await self.db.execute(income_stmt)
        income_by_category = {row[0]: row[1] for row in income_result.all()}

        expense_stmt = select(
            Transaction.category_id,
            func.sum(Transaction.amount).label('total')
        ).where(
            Transaction.owner_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.date >= start_date,
            Transaction.date <= end_date,
            Transaction.is_deleted == False
        ).group_by(Transaction.category_id)

        expense_result = await self.db.execute(expense_stmt)
        expense_by_category = {row[0]: row[1] for row in expense_result.all()}

        total_income = sum(income_by_category.values())
        total_expense = sum(expense_by_category.values())
        net_cash_flow = total_income - total_expense

        return CashFlowAnalysis(
            total_income=total_income,
            total_expense=total_expense,
            net_cash_flow=net_cash_flow,
            income_by_category=income_by_category,
            expense_by_category=expense_by_category,
            savings_rate=(net_cash_flow / total_income * 100) if total_income > 0 else 0
        )

    async def get_financial_health_score(self, user_id: int) -> FinancialHealth:
        total_balance = await self.get_total_balance(user_id)
        cash_flow = await self.get_cash_flow_analysis(
            user_id,
            datetime.utcnow() - timedelta(days=30),
            datetime.utcnow()
        )

        goals_stmt = select(Goal).where(Goal.owner_id == user_id)
        goals_result = await self.db.execute(goals_stmt)
        goals = goals_result.scalars().all()

        emergency_fund_months = 0
        if cash_flow.total_expense > 0:
            emergency_fund_months = total_balance["total_balance"] / cash_flow.total_expense

        debt_to_income = 0
        if cash_flow.total_income > 0:
            # Здесь можно добавить логику для учета долгов
            debt_to_income = 0

        score = 0
        factors = []

        if emergency_fund_months >= 6:
            score += 30
            factors.append("Отличный резервный фонд")
        elif emergency_fund_months >= 3:
            score += 20
            factors.append("Хороший резервный фонд")
        else:
            factors.append(f"Увеличьте резервный фонд (сейчас {emergency_fund_months:.1f} месяцев)")

        if cash_flow.savings_rate >= 20:
            score += 30
            factors.append("Отличная норма сбережений")
        elif cash_flow.savings_rate >= 10:
            score += 20
            factors.append("Хорошая норма сбережений")
        else:
            factors.append(f"Низкая норма сбережений: {cash_flow.savings_rate:.1f}%")

        completed_goals = sum(1 for goal in goals if goal.current_amount >= goal.target_amount)
        if goals:
            goal_progress = completed_goals / len(goals)
            if goal_progress >= 0.75:
                score += 20
                factors.append("Отличный прогресс по целям")
            elif goal_progress >= 0.5:
                score += 15
                factors.append("Хороший прогресс по целям")

        if len(total_balance["balance_by_account_type"]) >= 2:
            score += 20
            factors.append("Хорошая диверсификация счетов")

        return FinancialHealth(
            score=min(score, 100),
            factors=factors,
            emergency_fund_months=emergency_fund_months,
            savings_rate=cash_flow.savings_rate,
            recommendations=self._generate_recommendations(score, factors)
        )

    def _generate_recommendations(self, score: int, factors: List[str]) -> List[str]:
        recommendations = []

        if score < 50:
            recommendations.extend([
                "Создайте резервный фонд на 3-6 месяцев расходов",
                "Увеличьте норму сбережений до至少 10%",
                "Установите финансовые цели и отслеживайте прогресс"
            ])
        elif score < 80:
            recommendations.extend([
                "Рассмотрите инвестирование избыточных средств",
                "Диверсифицируйте типы счетов",
                "Оптимизируйте налоговые выплаты"
            ])
        else:
            recommendations.extend([
                "Поддерживайте текущие финансовые привычки",
                "Рассмотрите долгосрочные инвестиции",
                "Планируйте крупные финансовые цели"
            ])

        return recommendations