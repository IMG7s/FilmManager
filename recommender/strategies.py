from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Any

from core.entities.movie import Movie
from core.entities.user import User

from utils.movie_db import MovieDB
from utils.user_db import UserDB


# ============================================================
# БАЗОВЫЙ ИНТЕРФЕЙС СТРАТЕГИИ
# ============================================================

class RecommendationStrategy(ABC):
    @abstractmethod
    def recommend(
            self,
            movies: list[Movie],
            user: User = None,
            users: list[User] = None,
            **kwargs,
    ) -> list[Movie]:
        raise NotImplementedError


# ============================================================
# СТРАТЕГИЯ №1 — ПО ЖАНРАМ ПОЛЬЗОВАТЕЛЯ
# ============================================================

class UserGenreRecommendationStrategy(RecommendationStrategy):

    def __init__(self, top_n: int = 5):
        self.top_n = top_n

    def recommend(self, movies: list[Movie], user: User = None, **kwargs) -> list[Movie]:
        if user is None:
            raise ValueError("Стратегия жанров требует 'user'")

        favorite_genres = user.get_genres()

        matched = [
            movie for movie in movies
            if any(g in movie.genres for g in favorite_genres)
        ]

        matched.sort(key=lambda m: m.rating, reverse=True)

        return matched[:self.top_n]


# ============================================================
# СТРАТЕГИЯ №2 — САМЫЕ ПОПУЛЯРНЫЕ (ТОП ПО РЕЙТИНГУ)
# ============================================================

class RatingStrategy(RecommendationStrategy):

    def __init__(self, limit: int = 5):
        self.limit = limit

    def recommend(self, movies: list[Movie], **kwargs) -> list[Movie]:
        sorted_movies = sorted(movies, key=lambda m: m.rating, reverse=True)
        return sorted_movies[:self.limit]


# ============================================================
# СТРАТЕГИЯ №3 — ПОХОЖИЕ ПОЛЬЗОВАТЕЛИ
# ============================================================

class UserBasedRecommendationStrategy(RecommendationStrategy):

    def __init__(self, top_n: int = 5):
        self.top_n = top_n

    def recommend(
            self,
            movies: list[Movie],
            user: User = None,
            users: list[User] = None,
            **kwargs
    ) -> list[Movie]:

        if user is None or users is None:
            raise ValueError("Нужны user и users")

        target_genres = set(user.get_genres())

        similar_users = [
            u for u in users
            if u.id != user.id and len(target_genres.intersection(u.get_genres())) > 0
        ]

        candidate_movies: list[Movie] = []

        for u in similar_users:
            for m in movies:
                if any(g in u.get_genres() for g in m.genres):
                    candidate_movies.append(m)

        # сортировка по рейтингу
        candidate_movies.sort(key=lambda m: m.rating, reverse=True)

        # удаляем дубликаты по ID
        unique = list({m.id: m for m in candidate_movies}.values())

        return unique[:self.top_n]


# ============================================================
# ДВИЖОК РЕКОМЕНДАЦИЙ
# ============================================================

class RecommendationEngine:

    def __init__(self, strategy: RecommendationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: RecommendationStrategy):
        self._strategy = strategy

    def recommend(self, movies: list[Movie], **kwargs):
        return self._strategy.recommend(movies, **kwargs)


# ============================================================
# ТЕСТ РАБОТЫ
# ============================================================

if __name__ == "__main__":
    movie_db = MovieDB("/Users/ikhsan/PycharmProjects/FilmManager/test_movies.json")
    user_db = UserDB("/Users/ikhsan/PycharmProjects/FilmManager/test_users.json")

    movies = movie_db.db
    users = user_db.db

    print("\n=== Пользователи в БД ===")
    for u in users:
        print(u)

    # берём первого пользователя
    if users:
        current_user = users[0]
    else:
        raise ValueError("Нет пользователей в БД")

    print("\n=== Стратегия 1: По жанрам ===")
    engine = RecommendationEngine(UserGenreRecommendationStrategy(top_n=3))
    for m in engine.recommend(movies, user=current_user):
        print(m)

    print("\n=== Стратегия 2: Топ рейтинга ===")
    engine.set_strategy(RatingStrategy(limit=3))
    for m in engine.recommend(movies):
        print(m)

    print("\n=== Стратегия 3: Похожие пользователи ===")
    engine.set_strategy(UserBasedRecommendationStrategy(top_n=3))
    for m in engine.recommend(movies, user=current_user, users=users):
        print(m)
