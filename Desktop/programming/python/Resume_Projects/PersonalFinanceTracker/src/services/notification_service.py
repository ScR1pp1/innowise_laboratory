from enum import Enum
from datetime import datetime
from typing import List, Dict
import smtplib
from email.mime.text import MimeText

from sqlalchemy.ext.asyncio import AsyncSession


class NotificationType(Enum):
    BUDGET_ALERT = "budget_alert"
    GOAL_PROGRESS = "goal_progress"
    BILL_REMINDER = "bill_reminder"
    SECURITY_ALERT = "security_alert"
    FINANCIAL_TIP = "financial_tip"


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_and_send_alerts(self, user_id: int):
        """Проверяет условия и отправляет уведомления"""
        alerts = []

        budget_alerts = await self._check_budget_alerts(user_id)
        alerts.extend(budget_alerts)

        goal_alerts = await self._check_goal_alerts(user_id)
        alerts.extend(goal_alerts)

        account_alerts = await self._check_account_alerts(user_id)
        alerts.extend(account_alerts)

        for alert in alerts:
            await self._send_notification(user_id, alert)

    async def _check_budget_alerts(self, user_id: int) -> List[Dict]:
        """Проверяет превышение бюджетов"""
        # Логика проверки бюджетов
        pass

    async def _check_goal_alerts(self, user_id: int) -> List[Dict]:
        """Проверяет прогресс по целям"""
        # Логика проверки целей
        pass