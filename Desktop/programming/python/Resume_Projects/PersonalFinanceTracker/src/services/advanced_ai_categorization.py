import re
import json
from typing import Dict, List, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Transaction, Category


class AdvancedAICategorizationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = None
        self.vectorizer = None
        self.categories = []
        self._load_or_train_model()

    async def _load_or_train_model(self):
        """Загружает или тренирует модель категоризации"""
        try:
            self.model = joblib.load('models/categorization_model.pkl')
            self.vectorizer = joblib.load('models/vectorizer.pkl')
            with open('models/categories.json', 'r') as f:
                self.categories = json.load(f)
        except:
            await self._train_model()

    async def _train_model(self):
        """Тренирует модель на исторических данных пользователей"""
        stmt = select(Transaction, Category).join(
            Category, Transaction.category_id == Category.id
        ).where(
            Transaction.description.isnot(None),
            Category.name.isnot(None)
        ).limit(10000)

        result = await self.db.execute(stmt)
        data = result.all()

        if len(data) < 100:
            self.model = None
            return

        descriptions = []
        labels = []

        for transaction, category in data:
            if transaction.description and category.name:
                descriptions.append(transaction.description.lower())
                labels.append(category.name)

        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=['в', 'на', 'с', 'по', 'за', 'от', 'до']
        )

        self.model = Pipeline([
            ('tfidf', self.vectorizer),
            ('classifier', MultinomialNB())
        ])

        self.model.fit(descriptions, labels)
        self.categories = list(set(labels))

        import os
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, 'models/categorization_model.pkl')
        joblib.dump(self.vectorizer, 'models/vectorizer.pkl')
        with open('models/categories.json', 'w') as f:
            json.dump(self.categories, f)

    async def categorize_transaction(self, description: str, amount: float, user_id: int) -> Tuple[str, float]:
        """Категоризирует транзакцию с уверенностью"""
        if not self.model:
            return await self._rule_based_categorization(description, amount)

        try:
            probabilities = self.model.predict_proba([description.lower()])[0]
            predicted_index = probabilities.argmax()
            confidence = probabilities[predicted_index]
            category = self.categories[predicted_index]

            if confidence < 0.6:
                category = await self._rule_based_categorization(description, amount)
                confidence = 0.5

            return category, confidence
        except:
            return await self._rule_based_categorization(description, amount), 0.3

    async def _rule_based_categorization(self, description: str, amount: float) -> str:
        """Резервная категоризация на основе правил"""
        description_lower = description.lower()

        rules = {
            'food': [
                r'.*магазин.*', r'.*продукт.*', r'.*еда.*', r'.*супермаркет.*',
                r'.*ашан.*', r'.*пятерочка.*', r'.*перекресток.*', r'.*магнит.*',
                r'.*еда.*', r'.*продукты.*', r'.*бакалея.*'
            ],
            'transport': [
                r'.*бензин.*', r'.*заправка.*', r'.*такси.*', r'.*метро.*',
                r'.*автобус.*', r'.*транспорт.*', r'.*топливо.*', r'.*азс.*'
            ],
            'entertainment': [
                r'.*кино.*', r'.*ресторан.*', r'.*кафе.*', r'.*развлечен.*',
                r'.*отдых.*', r'.*бар.*', r'.*кофе.*', r'.*билет.*'
            ],
            'utilities': [
                r'.*коммунал.*', r'.*электричество.*', r'.*вода.*', r'.*интернет.*',
                r'.*телефон.*', r'.*квартплата.*', r'.*жкх.*'
            ],
            'health': [
                r'.*аптека.*', r'.*врач.*', r'.*больница.*', r'.*медицин.*',
                r'.*стоматолог.*', r'.*лекарств.*'
            ]
        }

        for category, patterns in rules.items():
            for pattern in patterns:
                if re.search(pattern, description_lower):
                    return category

        if amount < 500:
            return 'small_expenses'
        elif amount < 5000:
            return 'medium_expenses'
        else:
            return 'large_expenses'