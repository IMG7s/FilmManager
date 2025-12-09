from core.entities.movie import Movie
from utils.movie_db import MovieDB
from abc import ABC, abstractmethod


# --- Пользователи ---
class User:
    def __init__(self, user_id, name, favorite_genres):
        self.id = user_id
        self.name = name
        self.favorite_genres = favorite_genres


user = User(1, "ikhsan", ["ужасы", "комедия"])
user2 = User(2, "Tom", ["фантастика"])
user3 = User(3, "Jean", ["драма", "комедия"])


# --- Стратегия (абстрактная) ---
class RecommendationStrategy(ABC):
    @abstractmethod
    def recommend(self, movies, **kwargs):
        pass


# --- Стратегия №1: По жанрам ---
class UserGenreRecommendationStrategy(RecommendationStrategy):
    def recommend(self, movies, user=None, top_n=5, **kwargs):
        if user is None:
            raise ValueError("Для рекомендации по жанрам требуется user")

        favorite_genres = user.favorite_genres

        matched = [
            movie for movie in movies
            if any(g in movie.genres for g in favorite_genres)
        ]

        sorted_movies = sorted(matched, key=lambda m: m.rating, reverse=True)

        return sorted_movies[:top_n]


# --- Стратегия №2: По рейтингу ---
class RatingStrategy(RecommendationStrategy):
    def __init__(self, limit=5):
        self.limit = limit

    def recommend(self, movies, **kwargs):
        sorted_movies = sorted(
            movies,
            key=lambda m: m.rating,
            reverse=True
        )
        return sorted_movies[:self.limit]


# --- Движок рекомендаций ---
class RecommendationEngine:
    def __init__(self, strategy: RecommendationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def recommend(self, movies, **kwargs):
        return self.strategy.recommend(movies, **kwargs)



# ==============================
# ЗАГРУЗКА БАЗЫ ФИЛЬМОВ
# ==============================

db = MovieDB("/Users/ikhsan/PycharmProjects/FilmManager/test_movies.json")

movies = db.db      # ← вот список Movie, взятый из JSON


# ==============================
# ТЕСТ: рекомендация по жанрам
# ==============================

engine = RecommendationEngine(UserGenreRecommendationStrategy())

print("\nРекомендации по жанрам:")
recs = engine.recommend(movies, user=user, top_n=3)

for m in recs:
    print(m)


# ==============================
# ТЕСТ: рекомендация по рейтингу
# ==============================

engine.set_strategy(RatingStrategy(limit=3))

print("\nТоп по рейтингу:")
recs = engine.recommend(movies)

for m in recs:
    print(m)
