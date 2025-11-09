import asyncio
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.crud.transaction import transaction as crud_transaction
from src.models.budget import Budget
from src.models.tag import Tag
from src.models.transaction import Transaction
from src.schemas.analytics import AnalyticsRequest, AnalyticsResponse, CategoryAnalysis, FinancialSummary
from src.models.account import Account
from src.models.main import TransactionType as ModelTransactionType
from src.schemas.budget import BudgetAnalysis


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_financial_analytics(self, request: AnalyticsRequest, owner_id: int) -> AnalyticsResponse:
        transactions = await crud_transaction.get_transactions_by_period(
            db=self.db,
            owner_id=owner_id,
            start_date=request.start_date,
            end_date=request.end_date
        )

        if request.account_ids:
            transactions = [t for t in transactions if t.account_id in request.account_ids]
        if request.tag_ids:
            transactions = [t for t in transactions if any(tag.id in request.tag_ids for tag in t.tags)]

        income_transactions = [t for t in transactions if t.type.value == "income"]
        expense_transactions = [t for t in transactions if t.type.value == "expense"]

        total_income = sum(t.amount for t in income_transactions)
        total_expenses = sum(t.amount for t in expense_transactions)
        balance = total_income - total_expenses

        tag_analysis = await self._analyze_by_tags(expense_transactions)

        budget_status = await self._get_budget_status(owner_id, request.start_date, request.end_date)

        top_expenses = sorted(expense_transactions, key=lambda x: x.amount, reverse=True)[:10]

        return AnalyticsResponse(
            period_start=request.start_date,
            period_end=request.end_date,
            total_income=total_income,
            total_expenses=total_expenses,
            balance=balance,
            currency=None,
            by_tag=tag_analysis,
            budget_status=budget_status,
            top_expenses=top_expenses
        )

    @staticmethod
    async def _analyze_by_tags(transactions: List[Transaction]) -> List[CategoryAnalysis]:
        tag_totals = {}

        for transaction in transactions:
            for tag in transaction.tags:
                if tag.id not in tag_totals:
                    tag_totals[tag.id] = {"tag": tag, "amount": 0}
                tag_totals[tag.id]["amount"] += transaction.amount

        total_expenses = sum(item["amount"] for item in tag_totals.values())

        result = []
        for item in tag_totals.values():
            percentage = (item["amount"] / total_expenses * 100) if total_expenses > 0 else 0
            result.append(CategoryAnalysis(
                tag=item["tag"],
                amount=item["amount"],
                percentage=round(percentage, 2)
            ))

        return sorted(result, key=lambda x: x.amount, reverse=True)

    async def _get_budget_status(self, owner_id: int, start_date: datetime, end_date: datetime) -> List[BudgetAnalysis]:
        result = await self.db.execute(
            select(Budget).where(
                Budget.owner_id == owner_id,
                Budget.start_date <= end_date,
                Budget.end_date >= start_date
            )
        )
        budgets = result.scalars().all()

        budget_status = []
        for budget in budgets:
            spent = await self._calculate_budget_spending(budget, start_date, end_date)
            remaining = budget.amount - spent
            percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0

            budget_status.append(BudgetAnalysis(
                budget=budget,
                spent=spent,
                remaining=remaining,
                percentage_used=round(percentage_used, 2)
            ))

        return budget_status

    async def _calculate_budget_spending(self, budget: Budget, start_date: datetime, end_date: datetime) -> float:
        result = await self.db.execute(
            select(Transaction).where(
                Transaction.owner_id == budget.owner_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date,
                Transaction.type == ModelTransactionType.EXPENSE
            )
        )
        transactions = result.scalars().all()

        spent = 0
        for transaction in transactions:
            if budget.category_id and transaction.category_id == budget.category_id:
                spent += transaction.amount
            elif budget.tag_id and any(tag.id == budget.tag_id for tag in transaction.tags):
                spent += transaction.amount

        return spent

    async def get_financial_summary(self, owner_id: int) -> FinancialSummary:
        result = await self.db.execute(
            select(Account).where(
                Account.owner_id == owner_id,
                Account.is_active == True
            )
        )
        accounts = result.scalars().all()

        total_balance = sum(account.balance for account in accounts)

        end_date = datetime.utcnow()
        if end_date.month > 1:
            start_date = datetime(end_date.year, end_date.month - 1, end_date.day)
        else:
            start_date = datetime(end_date.year - 1, 12, end_date.day)

        transactions = await crud_transaction.get_transactions_by_period(
            db=self.db,
            owner_id=owner_id,
            start_date=start_date,
            end_date=end_date
        )

        total_income = sum(t.amount for t in transactions if t.type.value == "income")
        total_expenses = sum(t.amount for t in transactions if t.type.value == "expense")

        upcoming_bills = [
            t for t in transactions
            if t.type.value == "expense" and t.date > datetime.utcnow()
        ][:5]

        return FinancialSummary(
            total_balance=total_balance,
            total_income=total_income,
            total_expenses=total_expenses,
            net_worth=total_balance + total_income - total_expenses,
            account_balances=[{"id": acc.id, "name": acc.name, "balance": acc.balance} for acc in accounts],
            upcoming_bills=upcoming_bills
        )