# src/services/validation_service.py
from decimal import Decimal
from datetime import datetime
from src.models import Account
from src.models.main import TransactionType


class ValidationService:
    @staticmethod
    def validate_transaction_amount(amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > 1_000_000_000:
            raise ValueError("Amount too large")
        return True

    @staticmethod
    def validate_account_balance(account: Account, amount: float, transaction_type: TransactionType) -> bool:
        if transaction_type == TransactionType.EXPENSE and account.balance < amount:
            raise ValueError("Insufficient funds")
        return True

    @staticmethod
    def validate_transaction_date(date: datetime) -> bool:
        if date > datetime.utcnow():
            raise ValueError("Future dates are not allowed")
        if date < datetime(2000, 1, 1):
            raise ValueError("Date too far in the past")
        return True