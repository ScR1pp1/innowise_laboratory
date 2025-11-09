# src/services/advanced_ai_prediction.py
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Transaction


class AdvancedAIPredictionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def predict_financial_future(self, user_id: int, months: int = 6) -> Dict:
        """Комплексное предсказание финансового будущего"""
        historical_data = await self._get_historical_data(user_id, months * 2)

        if len(historical_data) < 3:
            return await self._get_basic_prediction(user_id, months)

        df = self._prepare_time_series_data(historical_data)

        predictions = {
            'expenses': await self._predict_expenses(df, months),
            'income': await self._predict_income(df, months),
            'savings': await self._predict_savings(df, months),
            'anomalies': await self._detect_anomalies(df),
            'seasonal_patterns': await self._analyze_seasonality(df)
        }

        return predictions

    async def _get_historical_data(self, user_id: int, months: int) -> List[Dict]:
        """Получает исторические данные за указанный период"""
        start_date = datetime.utcnow() - timedelta(days=months * 30)

        stmt = select(Transaction).where(
            Transaction.owner_id == user_id,
            Transaction.date >= start_date,
            Transaction.is_deleted == False
        )
        result = await self.db.execute(stmt)
        transactions = result.scalars().all()

        return [
            {
                'date': t.date,
                'amount': t.amount,
                'type': t.type.value,
                'category_id': t.category_id
            }
            for t in transactions
        ]

    def _prepare_time_series_data(self, data: List[Dict]) -> pd.DataFrame:
        """Подготавливает данные для временных рядов"""
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')

        daily = df.groupby([pd.Grouper(freq='D'), 'type'])['amount'].sum().unstack(fill_value=0)
        daily = daily.reindex(pd.date_range(start=daily.index.min(), end=daily.index.max(), freq='D'), fill_value=0)

        return daily

    async def _predict_expenses(self, df: pd.DataFrame, months: int) -> Dict:
        """Предсказывает расходы с использованием нескольких моделей"""
        if 'expense' not in df.columns:
            return {'predicted': 0, 'confidence': 0, 'trend': 'stable'}

        expenses = df['expense'].replace(0, np.nan).ffill().bfill()

        X = np.array(range(len(expenses))).reshape(-1, 1)
        y = expenses.values

        model = LinearRegression()
        model.fit(X, y)

        future_X = np.array(range(len(expenses), len(expenses) + months * 30)).reshape(-1, 1)
        future_predictions = model.predict(future_X)

        future_predictions = np.maximum(future_predictions, 0)

        return {
            'predicted_monthly': np.mean(future_predictions) * 30,
            'confidence': max(0, model.score(X, y)),
            'trend': 'up' if model.coef_[0] > 0 else 'down',
            'daily_predictions': future_predictions.tolist()
        }

    async def _detect_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """Обнаруживает аномальные траты"""
        if 'expense' not in df.columns:
            return []

        expenses = df['expense']
        Q1 = expenses.quantile(0.25)
        Q3 = expenses.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        anomalies = []
        for date, amount in expenses.items():
            if amount > upper_bound:
                anomalies.append({
                    'date': date,
                    'amount': amount,
                    'reason': 'unusually_high_spending',
                    'severity': 'high' if amount > upper_bound * 2 else 'medium'
                })

        return anomalies

    async def _analyze_seasonality(self, df: pd.DataFrame) -> Dict:
        """Анализирует сезонные паттерны"""
        if 'expense' not in df.columns:
            return {}

        expenses = df['expense']

        daily_pattern = expenses.groupby(expenses.index.dayofweek).mean()

        monthly_pattern = expenses.groupby(expenses.index.month).mean()

        return {
            'daily_pattern': {
                day: amount for day, amount in daily_pattern.items()
            },
            'monthly_pattern': {
                month: amount for month, amount in monthly_pattern.items()
            },
            'peak_spending_day': daily_pattern.idxmax(),
            'peak_spending_month': monthly_pattern.idxmax()
        }