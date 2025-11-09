from typing import Dict, List, Optional
import aiohttp
import asyncio
from datetime import datetime, timedelta
import hashlib
import hmac

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import Transaction
from src.models.main import TransactionType
from src.services.advanced_ai_categorization import AdvancedAICategorizationService


class OpenBankingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.providers = {
            'sberbank': SberbankAPI(),
            'tinkoff': TinkoffAPI(),
            'alfa': AlfaBankAPI(),
        }

    async def connect_bank_account(self, user_id: int, bank_name: str, credentials: Dict) -> str:
        """Подключает банковский счет через Open Banking API"""
        provider = self.providers.get(bank_name)
        if not provider:
            raise ValueError(f"Unsupported bank: {bank_name}")

        consent_id = await provider.create_consent(credentials)

        connection = BankConnection(
            user_id=user_id,
            bank_name=bank_name,
            consent_id=consent_id,
            is_active=True,
            connected_at=datetime.utcnow()
        )
        self.db.add(connection)
        await self.db.commit()

        return consent_id

    async def sync_bank_transactions(self, user_id: int, bank_name: str) -> List[Transaction]:
        """Синхронизирует транзакции из банка"""
        connection = await self._get_active_connection(user_id, bank_name)
        if not connection:
            raise ValueError("No active connection found")

        provider = self.providers[bank_name]

        # Получаем транзакции за последние 30 дней
        transactions_data = await provider.get_transactions(
            connection.consent_id,
            since=datetime.utcnow() - timedelta(days=30)
        )

        transactions = []
        categorization_service = AdvancedAICategorizationService(self.db)

        for tx_data in transactions_data:
            existing = await self._find_existing_transaction(tx_data['id'])
            if existing:
                continue

            category, confidence = await categorization_service.categorize_transaction(
                tx_data['description'], tx_data['amount'], user_id
            )

            transaction = Transaction(
                amount=tx_data['amount'],
                description=tx_data['description'],
                date=tx_data['date'],
                type=TransactionType.EXPENSE if tx_data['amount'] < 0 else TransactionType.INCOME,
                account_id=await self._get_or_create_account(user_id, tx_data['account']),
                owner_id=user_id,
                bank_transaction_id=tx_data['id'],
                currency=tx_data.get('currency', 'RUB')
            )

            transactions.append(transaction)

        self.db.add_all(transactions)
        await self.db.commit()

        return transactions


class TinkoffAPI:
    def __init__(self):
        self.base_url = "https://api.tinkoff.ru/openapi/"
        self.client_id = settings.TINKOFF_CLIENT_ID
        self.client_secret = settings.TINKOFF_CLIENT_SECRET

    async def create_consent(self, credentials: Dict) -> str:
        """Создает согласие на доступ к данным"""
        async with aiohttp.ClientSession() as session:
            headers = self._get_auth_headers()
            payload = {
                "customer": {
                    "phone": credentials['phone']
                },
                "permissions": ["accounts", "transactions"]
            }

            async with session.post(
                    f"{self.base_url}/consents",
                    headers=headers,
                    json=payload
            ) as response:
                data = await response.json()
                return data['consent_id']

    async def get_transactions(self, consent_id: str, since: datetime) -> List[Dict]:
        """Получает транзакции по согласию"""
        async with aiohttp.ClientSession() as session:
            headers = self._get_auth_headers()

            async with session.get(
                    f"{self.base_url}/transactions",
                    headers=headers,
                    params={
                        "consent_id": consent_id,
                        "from": since.isoformat()
                    }
            ) as response:
                data = await response.json()
                return self._normalize_transactions(data['transactions'])

    def _normalize_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """Нормализует транзакции из банковского API в наш формат"""
        normalized = []

        for tx in transactions:
            normalized.append({
                'id': tx['id'],
                'amount': abs(tx['amount']),
                'description': tx['description'],
                'date': datetime.fromisoformat(tx['date']),
                'account': tx['account'],
                'currency': tx.get('currency', 'RUB')
            })

        return normalized