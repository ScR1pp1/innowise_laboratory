import logging
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import aiosmtplib
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import Budget
from src.services.advanced_ai_prediction import AdvancedAIPredictionService


class NotificationChannel(Enum):
    EMAIL = "email"
    TELEGRAM = "telegram"
    IN_APP = "in_app"


class NotificationPriority(Enum):
    URGENT = "urgent"
    IMPORTANT = "important"
    INFO = "info"


@dataclass
class Notification:
    id: str
    user_id: int
    title: str
    message: str
    priority: NotificationPriority
    channel: NotificationChannel
    created_at: datetime
    is_read: bool = False
    action_url: Optional[str] = None


class AdvancedNotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_and_send_alerts(self, user_id: int):
        """Проверяет все условия и отправляет уведомления"""
        notifications = []

        budget_notifications = await self._check_budget_alerts(user_id)
        notifications.extend(budget_notifications)

        goal_notifications = await self._check_goal_alerts(user_id)
        notifications.extend(goal_notifications)

        account_notifications = await self._check_account_alerts(user_id)
        notifications.extend(account_notifications)

        ai_notifications = await self._check_ai_alerts(user_id)
        notifications.extend(ai_notifications)

        for notification in notifications:
            await self._save_notification(notification)
            await self._send_notification(notification)

    async def _check_budget_alerts(self, user_id: int) -> List[Notification]:
        """Проверяет превышение бюджетов"""
        alerts = []
        today = datetime.utcnow()

        stmt = select(Budget).where(
            Budget.owner_id == user_id,
            Budget.start_date <= today,
            Budget.end_date >= today
        )
        result = await self.db.execute(stmt)
        budgets = result.scalars().all()

        for budget in budgets:
            spent = await self._calculate_budget_spending(budget)
            utilization = spent / budget.amount if budget.amount > 0 else 0

            if utilization >= 0.9:
                alerts.append(Notification(
                    id=f"budget_alert_{budget.id}",
                    user_id=user_id,
                    title="⚠️ Бюджет почти исчерпан",
                    message=f"Бюджет '{budget.name}' использован на {utilization * 100:.1f}%",
                    priority=NotificationPriority.URGENT,
                    channel=NotificationChannel.IN_APP,
                    created_at=datetime.utcnow()
                ))
            elif utilization >= 0.7:
                alerts.append(Notification(
                    id=f"budget_warning_{budget.id}",
                    user_id=user_id,
                    title="📊 Бюджет используется активно",
                    message=f"Бюджет '{budget.name}' использован на {utilization * 100:.1f}%",
                    priority=NotificationPriority.IMPORTANT,
                    channel=NotificationChannel.IN_APP,
                    created_at=datetime.utcnow()
                ))

        return alerts

    async def _check_ai_alerts(self, user_id: int) -> List[Notification]:
        """AI-уведомления на основе анализа данных"""
        alerts = []
        prediction_service = AdvancedAIPredictionService(self.db)
        predictions = await prediction_service.predict_financial_future(user_id)

        for anomaly in predictions.get('anomalies', []):
            if anomaly['severity'] == 'high':
                alerts.append(Notification(
                    id=f"anomaly_{anomaly['date'].timestamp()}",
                    user_id=user_id,
                    title="🚨 Необычная трата",
                    message=f"Обнаружена необычно высокая трата: {anomaly['amount']} руб.",
                    priority=NotificationPriority.URGENT,
                    channel=NotificationChannel.IN_APP,
                    created_at=datetime.utcnow()
                ))

        seasonal_patterns = predictions.get('seasonal_patterns', {})
        if seasonal_patterns.get('peak_spending_month') == datetime.utcnow().month:
            alerts.append(Notification(
                id="seasonal_alert",
                user_id=user_id,
                title="📈 Сезон высоких расходов",
                message="Этот месяц исторически является пиковым для ваших расходов. Будьте внимательны к бюджету.",
                priority=NotificationPriority.IMPORTANT,
                channel=NotificationChannel.IN_APP,
                created_at=datetime.utcnow()
            ))

        return alerts

    async def _send_notification(self, notification: Notification):
        """Отправляет уведомление через выбранный канал"""
        try:
            if notification.channel == NotificationChannel.EMAIL:
                await self._send_email(notification)
            elif notification.channel == NotificationChannel.TELEGRAM:
                await self._send_telegram(notification)
            elif notification.channel == NotificationChannel.IN_APP:
                await self._store_in_app(notification)
        except Exception as e:
            logging.error(f"Failed to send notification: {e}")

    async def _send_email(self, notification: Notification):
        """Отправляет email уведомление"""
        message = MimeMultipart()
        message["From"] = "noreply@financetracker.com"
        message["To"] = await self._get_user_email(notification.user_id)
        message["Subject"] = notification.title

        body = f"""
        {notification.message}

        Приоритет: {notification.priority.value}
        Дата: {notification.created_at.strftime('%Y-%m-%d %H:%M')}
        """
        message.attach(MimeText(body, "plain"))

        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD
        )