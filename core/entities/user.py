import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List, Dict

from core.entities.movie import Movie


class User:
    def __init__(self, user_name: str, user_password: str) -> None:
        self.__password = user_password
        self.user_name = user_name
        self._id = 0
        self.user_prefer = set()

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value

    def addGenre(self, genres: List) -> str:
        if isinstance(genres, list):
            added_count = 0
            for genre in genres:
                if genre in Movie.allowed_genres:
                    self.user_prefer.add(genre)
                    added_count += 1

            if added_count == 0:
                return "Не добавлено ни одного жанра (возможно, недопустимые жанры)"
            return f"Добавлено {added_count} жанров"
        else:
            return "Нужно подать список"

    def get_genres(self) -> List[str]:
        """Получить список предпочтений."""
        return list(self.user_prefer)

    def to_dict(self) -> Dict:
        """Преобразовать в словарь для сохранения."""
        return {
            "id": self._id,
            "user_name": self.user_name,
            "password": self.__password,
            "genres": list(self.user_prefer),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "User":
        """Создать объект User из словаря."""
        user = cls(user_name=data["user_name"], user_password=data["password"])
        user._id = data.get("id", 0)

        genres_list = data.get("genres", [])
        if isinstance(genres_list, list):
            user.user_prefer = set(genres_list)
        else:
            user.user_prefer = set()

        return user

    def __str__(self) -> str:
        return f"id: {self._id}\nName: {self.user_name}\nGenres: {self.user_prefer}"
