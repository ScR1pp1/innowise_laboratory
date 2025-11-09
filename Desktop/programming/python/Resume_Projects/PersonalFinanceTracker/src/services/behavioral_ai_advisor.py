from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum
import random

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.financial_analytics import FinancialAnalyticsService


class AdvicePriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class UserFinancialProfile(Enum):
    AGGRESSIVE = "aggressive"
    MODERATE = "moderate"
    CONSERVATIVE = "conservative"


@dataclass
class AdvancedFinancialAdvice:
    title: str
    description: str
    priority: AdvicePriority
    action_steps: List[str]
    estimated_impact: str
    timeframe: str
    success_probability: float
    behavioral_nudge: str


class BehavioralAIAdvisorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.analytics_service = FinancialAnalyticsService(db)
        self.prediction_service = AdvancedAIPredictionService(db)

    async def generate_personalized_advice(self, user_id: int) -> List[AdvancedFinancialAdvice]:
        """Генерирует персонализированные советы с учетом профиля пользователя"""
        user_profile = await self._analyze_user_profile(user_id)
        financial_health = await self.analytics_service.get_financial_health_score(user_id)
        predictions = await self.prediction_service.predict_financial_future(user_id)

        advice_pool = await self._get_advice_pool()
        personalized_advice = []

        for advice_template in advice_pool:
            if await self._should_apply_advice(advice_template, user_profile, financial_health, predictions):
                advice = await self._customize_advice(advice_template, user_profile, financial_health)
                personalized_advice.append(advice)

        personalized_advice.sort(key=lambda x: (x.priority.value, x.success_probability), reverse=True)

        return personalized_advice[:5]

    async def _analyze_user_profile(self, user_id: int) -> UserFinancialProfile:
        """Анализирует финансовый профиль пользователя"""
        cash_flow = await self.analytics_service.get_cash_flow_analysis(
            user_id,
            datetime.utcnow() - timedelta(days=90),
            datetime.utcnow()
        )

        income_variability = await self._calculate_income_variability(user_id)

        risk_tolerance = await self._assess_risk_tolerance(user_id)

        if risk_tolerance > 0.7 and income_variability < 0.3:
            return UserFinancialProfile.AGGRESSIVE
        elif risk_tolerance < 0.3:
            return UserFinancialProfile.CONSERVATIVE
        else:
            return UserFinancialProfile.MODERATE

    async def _get_advice_pool(self) -> List[Dict]:
        """Возвращает пул возможных советов"""
        return [
            {
                'id': 'emergency_fund',
                'conditions': {'emergency_fund_months': lambda x: x < 3},
                'templates': {
                    UserFinancialProfile.CONSERVATIVE: AdvancedFinancialAdvice(
                        title="Создайте надежный резервный фонд",
                        description="Рекомендуем накопить 6 месяцев расходов для полной финансовой безопасности",
                        priority=AdvicePriority.CRITICAL,
                        action_steps=["Откладывайте 10% от каждого дохода", "Создайте отдельный сберегательный счет"],
                        estimated_impact="Высокая",
                        timeframe="3-6 месяцев",
                        success_probability=0.8,
                        behavioral_nudge="Автоматизируйте переводы на сбережения в день получения зарплаты"
                    ),
                    UserFinancialProfile.AGGRESSIVE: AdvancedFinancialAdvice(
                        title="Минимальный резервный фонд",
                        description="Достаточно 3 месяцев расходов, остальные средства можно инвестировать",
                        priority=AdvicePriority.HIGH,
                        action_steps=["Накопите 3 месяца расходов", "Остальные средства направьте в инвестиции"],
                        estimated_impact="Средняя",
                        timeframe="1-2 месяца",
                        success_probability=0.9,
                        behavioral_nudge="Установите цель и отслеживайте прогресс в реальном времени"
                    )
                }
            },
            {
                'id': 'savings_rate',
                'conditions': {'savings_rate': lambda x: x < 15},
                'templates': {
                    UserFinancialProfile.CONSERVATIVE: AdvancedFinancialAdvice(
                        title="Повысьте норму сбережений",
                        description="Цель - 20% от дохода. Начните с малого и постепенно увеличивайте",
                        priority=AdvicePriority.HIGH,
                        action_steps=["Проанализируйте основные статьи расходов", "Сократите 2-3 необязательные траты"],
                        estimated_impact="Высокая",
                        timeframe="1 месяц",
                        success_probability=0.7,
                        behavioral_nudge="Используйте правило 'сначала заплати себе'"
                    )
                }
            },
            {
                'id': 'investment',
                'conditions': {'emergency_fund_months': lambda x: x >= 6, 'savings_rate': lambda x: x > 15},
                'templates': {
                    UserFinancialProfile.MODERATE: AdvancedFinancialAdvice(
                        title="Начните инвестировать",
                        description="Избыточные сбережения должны работать на вас",
                        priority=AdvicePriority.MEDIUM,
                        action_steps=["Изучите основы инвестирования", "Начните с ETF фондов",
                                      "Диверсифицируйте портфель"],
                        estimated_impact="Высокая (долгосрочная)",
                        timeframe="6-12 месяцев",
                        success_probability=0.6,
                        behavioral_nudge="Начните с маленьких сумм чтобы преодолеть страх потерь"
                    )
                }
            }
        ]