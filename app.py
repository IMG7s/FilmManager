from __future__ import annotations

import os
from typing import Optional

from utils.movie_db import MovieDB
from core.entities.movie import Movie
# from recommender import (
#     GenreBasedStrategy,
#     RatingBasedStrategy,
#     SimilarUsersStrategy,
# )

# ===== Цвета ANSI =====
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


class ConsoleUser:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ratings: dict[int, float] = {}      # {movie_id: score}
        self.preferred_genres: list[str] = []    # любимые жанры (строки)

    def rate(self, movie_id: int, score: float) -> None:
        self.ratings[movie_id] = score

    def get_rating(self, movie_id: int) -> Optional[float]:
        return self.ratings.get(movie_id)

    def set_preferences(self, genres: list[str]) -> None:
        self.preferred_genres = genres


class ConsoleApp:
    def __init__(self) -> None:
        # JSON лежит рядом с app.py
        self._db = MovieDB("test_movies.json")

        # фильмы уже загружены в MovieDB.load_db() → берём из self._db.db
        self._movies: list[Movie] = self._db.db

        # пользователи в памяти
        self._users: dict[str, ConsoleUser] = {}
        self._current_user: Optional[ConsoleUser] = None

        # паттерн Strategy (Блок 2)
        # self._strategies = {
        #     "1": GenreBasedStrategy(),
        #     "2": RatingBasedStrategy(),
        #     "3": SimilarUsersStrategy(),
        # }

    # ================== ГЛАВНЫЙ ЦИКЛ ==================

    def run(self) -> None:
        while True:
            clear_screen()
            self._print_menu()
            choice = input(YELLOW + "Ваш выбор: " + RESET).strip()

            if choice == "1":
                self._register()
            elif choice == "2":
                self._login()
            elif choice == "3":
                self._show_movies()
            elif choice == "4":
                self._rate_movie()
            elif choice == "5":
                self._recommend_menu()
            elif choice == "6":
                self._set_preferences()
            elif choice == "0":
                print(MAGENTA + "Выход из приложения..." + RESET)
                break
            else:
                print(RED + "Неизвестная команда.\n" + RESET)
            input(YELLOW + "Нажмите Enter, чтобы продолжить..." + RESET)

    def _print_menu(self) -> None:
        print(CYAN + "=" * 40 + RESET)
        print(MAGENTA + "РЕКОМЕНДАТЕЛЬНАЯ СИСТЕМА ФИЛЬМОВ" + RESET)
        print(CYAN + "=" * 40 + RESET)
        user_name = self._current_user.name if self._current_user else "[нет]"
        print(f"Текущий пользователь: {GREEN}{user_name}{RESET}")
        print("-" * 40)
        print("1. Регистрация")
        print("2. Вход")
        print("3. Просмотр фильмов")
        print("4. Оценить фильм")
        print("5. Получить рекомендации")
        print("6. Настроить предпочтения по жанрам")
        print("0. Выход")
        print("-" * 40)

    def _register(self) -> None:
        name = input("Введите имя нового пользователя: ").strip()
        if not name:
            print(RED + "Имя не может быть пустым.\n" + RESET)
            return
        if name in self._users:
            print(RED + "Такой пользователь уже существует.\n" + RESET)
            return

        user = ConsoleUser(name)
        self._users[name] = user
        self._current_user = user
        print(GREEN + f"Пользователь '{name}' зарегистрирован и авторизован.\n" + RESET)

    def _login(self) -> None:
        name = input("Введите имя пользователя: ").strip()
        user = self._users.get(name)
        if not user:
            print(RED + "Пользователь не найден.\n" + RESET)
            return

        self._current_user = user
        print(GREEN + f"Вы вошли как '{name}'.\n" + RESET)

    def _show_movies(self) -> None:
        if not self._movies:
            print(RED + "Список фильмов пуст.\n" + RESET)
            return

        print("\n" + CYAN + "Список фильмов:" + RESET)
        print("-" * 40)
        for m in self._movies:
            print(f"[{m.id}] {m.title} ({m.year}) — рейтинг: {m.rating}")
        print()

    def _rate_movie(self) -> None:
        if not self._ensure_logged_in():
            return

        self._show_movies()
        raw_id = input("Введите ID фильма: ").strip()
        try:
            movie_id = int(raw_id)
        except ValueError:
            print(RED + "Некорректный ID.\n" + RESET)
            return

        movie = self._db.get_by_id(movie_id)
        if not movie:
            print(RED + "Фильм с таким ID не найден.\n" + RESET)
            return

        raw_score = input("Введите оценку (1–10): ").strip()
        try:
            score = float(raw_score)
        except ValueError:
            print(RED + "Некорректная оценка.\n" + RESET)
            return

        if not (1 <= score <= 10):
            print(RED + "Оценка должна быть от 1 до 10.\n" + RESET)
            return

        self._current_user.rate(movie_id, score)
        print(GREEN + f"Вы поставили фильму '{movie.title}' оценку {score}.\n" + RESET)

    def _set_preferences(self) -> None:
        if not self._ensure_logged_in():
            return

        # собираем все жанры из фильмов
        all_genres: set[str] = set()
        for m in self._movies:
            for g in m.genres:
                all_genres.add(g)

        if not all_genres:
            print(RED + "Жанры не найдены.\n" + RESET)
            return

        genres_list = sorted(all_genres)
        print("\n" + CYAN + "Доступные жанры:" + RESET)
        for i, g in enumerate(genres_list, start=1):
            print(f"{i}. {g}")

        raw = input(
            "Введите номера любимых жанров через запятую (например, 1,3,5): "
        ).strip()
        if not raw:
            print(YELLOW + "Предпочтения не изменены.\n" + RESET)
            return

        try:
            indices = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            print(RED + "Некорректный ввод.\n" + RESET)
            return

        selected: list[str] = []
        for idx in indices:
            if 1 <= idx <= len(genres_list):
                selected.append(genres_list[idx - 1])

        if not selected:
            print(RED + "Не выбрано ни одного жанра.\n" + RESET)
            return

        self._current_user.set_preferences(selected)
        print(GREEN + "Предпочтения по жанрам обновлены.\n" + RESET)

    def _recommend_menu(self) -> None:
        if not self._ensure_logged_in():
            return

        print(CYAN + "Выберите стратегию:" + RESET)
        print("1. По любимым жанрам пользователя")
        print("2. Фильмы с наивысшим рейтингом")
        print("3. На основе похожих пользователей")
        choice = input(YELLOW + "Ваш выбор: " + RESET).strip()

        strategy = self._strategies.get(choice)
        if not strategy:
            print(RED + "Неизвестная стратегия.\n" + RESET)
            return

        min_rating = self._ask_optional_float(
            "Минимальный рейтинг (Enter — без фильтра): "
        )
        min_year = self._ask_optional_int(
            "Минимальный год выпуска (Enter — без фильтра): "
        )

        recommended = strategy.recommend(self._movies, self._current_user, self._users)
        recommended = self._apply_filters(recommended, min_rating, min_year)

        if not recommended:
            print(RED + "Подходящих фильмов нет.\n" + RESET)
            return

        print("\n" + CYAN + "Рекомендованные фильмы:" + RESET)
        print("-" * 40)
        for m in recommended:
            print(f"[{m.id}] {m.title} ({m.year}) — рейтинг: {m.rating}")
        print()

    def _ensure_logged_in(self) -> bool:
        if self._current_user is None:
            print(RED + "Сначала войдите или зарегистрируйтесь.\n" + RESET)
            return False
        return True

    @staticmethod
    def _apply_filters(
        movies: list[Movie],
        min_rating: Optional[float],
        min_year: Optional[int],
    ) -> list[Movie]:
        result: list[Movie] = []
        for m in movies:
            if min_rating is not None and m.rating < min_rating:
                continue
            if min_year is not None and m.year < min_year:
                continue
            result.append(m)
        return result

    @staticmethod
    def _ask_optional_float(prompt: str) -> Optional[float]:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return float(value)
        except ValueError:
            print(YELLOW + "Фильтр по рейтингу отключён." + RESET)
            return None

    @staticmethod
    def _ask_optional_int(prompt: str) -> Optional[int]:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print(YELLOW + "Фильтр по году отключён." + RESET)
            return None


if __name__ == "__main__":
    app = ConsoleApp()
    app.run()
