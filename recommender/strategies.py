from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from core.entities.movie import Movie


class RecommendationStrategy(ABC):
    @abstractmethod
    def recommend(
            self,
            movies: list[Movie],
            user: Any = None,
            users: Any = None,
            **kwargs,
    ) -> list[Movie]:
        """Вернуть список рекомендованных фильмов."""
        raise NotImplementedError


class UserGenreRecommendationStrategy(RecommendationStrategy):
    """
    Стратегия №1: рекомендации по любимым жанрам пользователя.
    Работает с:
      - user.favorite_genres  ИЛИ
      - user.preferred_genres (как в ConsoleUser)
    """

    def __init__(self, top_n: int = 5) -> None:
        self.top_n = top_n

    def recommend(
            self,
            movies: list[Movie],
            user: Any = None,
            **kwargs,
    ) -> list[Movie]:
        if user is None:
            raise ValueError("Для рекомендации по жанрам требуется user")

        # Пытаемся взять favorite_genres, если нет — preferred_genres
        favorite_genres = getattr(user, "favorite_genres", None)
        if favorite_genres is None:
            favorite_genres = getattr(user, "preferred_genres", [])

        matched = [
            movie
            for movie in movies
            if any(g in movie.genres for g in favorite_genres)
        ]

        sorted_movies = sorted(matched, key=lambda m: m.rating, reverse=True)
        return sorted_movies[: self.top_n]


class RatingStrategy(RecommendationStrategy):
    """
    Стратегия №2: просто топ фильмов по рейтингу.
    """

    def __init__(self, limit: int = 5) -> None:
        self.limit = limit

    def recommend(
            self,
            movies: list[Movie],
            **kwargs,
    ) -> list[Movie]:
        sorted_movies = sorted(
            movies,
            key=lambda m: m.rating,
            reverse=True,
        )
        return sorted_movies[: self.limit]


class RecommendationEngine:
    """
    Движок рекомендаций, который использует текущую стратегию.
    """

    def __init__(self, strategy: RecommendationStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: RecommendationStrategy) -> None:
        self._strategy = strategy

    def recommend(self, movies: list[Movie], **kwargs) -> list[Movie]:
        return self._strategy.recommend(movies, **kwargs)
