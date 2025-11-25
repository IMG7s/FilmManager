import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from typing import Dict, List, Optional
from core.entities.movie import Movie


class MovieDB:
    """
    Хранилище фильмов
    Работает с объектами Movie
    """

    def __init__(self, db_path: str):
        self._db_path = db_path

        # список всех фильмов
        self.db: List[Movie] = []

        # индексы для ускорения поиска
        self.by_id: Dict[int, Movie] = {}
        self.by_title: Dict[str, Movie] = {}

        # загрузка базы
        self.load_db()

    # ---
    # ЗАГРУЗКА И СОХРАНЕНИЕ
    # ---

    def load_db(self):
        """Загружает JSON и превращает каждый словарь в Movie-объект."""

        try:
            with open(self._db_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            print("База не найдена — создаю новую.")
            raw_data = []
        except json.JSONDecodeError:
            print("Ошибка в JSON — создаю пустую базу.")
            raw_data = []

        self.db = []
        self.by_id = {}
        self.by_title = {}

        for item in raw_data:
            try:
                movie = Movie.from_dict(item)
                self._add_to_memory(movie)
            except Exception as e:
                print(f"Пропущена запись: {item} ({e})")

        print("База загружена, фильмов:", len(self.db))

    def save(self):
        """Сохраняет базу в JSON."""
        data = [movie.to_dict() for movie in self.db]

        with open(self._db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("База сохранена.")

    # ---
    # ВНУТРЕННИЕ ОПЕРАЦИИ
    # ---

    def _add_to_memory(self, movie: Movie):
        """Добавляет фильм в память и индексы."""
        self.db.append(movie)
        self.by_id[movie.id] = movie
        self.by_title[movie.title.lower()] = movie

    def _remove_from_memory(self, movie: Movie):
        """Удаляет фильм из памяти и индексов."""
        self.db.remove(movie)
        self.by_id.pop(movie.id, None)
        self.by_title.pop(movie.title.lower(), None)

    # ---
    # ПУБЛИЧНЫЕ CRUD ОПЕРАЦИИ
    # ---

    def add(self, movie: Movie):
        """Добавляет новый фильм."""
        if movie.id in self.by_id:
            raise ValueError("Фильм с таким ID уже существует.")

        self._add_to_memory(movie)
        self.save()

    def delete(self, movie_id: int):
        """Удаляет фильм по ID."""
        movie = self.by_id.get(movie_id)
        if not movie:
            raise ValueError("Фильм с таким ID не найден.")

        self._remove_from_memory(movie)
        self.save()

    def update(self, movie: Movie):
        """
        Обновляет фильм c тем же ID.
        Т.е. заменяет объект, если он существует.
        """
        if movie.id not in self.by_id:
            raise ValueError("Такого фильма нет, обновить нельзя.")

        # удаляем старый
        old = self.by_id[movie.id]
        self._remove_from_memory(old)

        # добавляем новый
        self._add_to_memory(movie)
        self.save()

    # ---
    # ПОИСК
    # ---

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return self.by_id.get(movie_id)

    def get_by_title(self, title: str) -> Optional[Movie]:
        return self.by_title.get(title.lower())

    def find_by_genre(self, genre: str) -> List[Movie]:
        return [m for m in self.db if genre in m.genres]

    # ---
    # СОРТИРОВКА
    # ---

    def sort_by_rating(self, reverse: bool = True) -> List[Movie]:
        return sorted(self.db, key=lambda m: m.rating, reverse=reverse)

    def sort_by_year(self, reverse: bool = False) -> List[Movie]:
        return sorted(self.db, key=lambda m: m.year, reverse=reverse)

    # ---

    def print_all(self):
        for m in self.db:
            print(m)
