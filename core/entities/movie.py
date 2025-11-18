from typing import List


class Movie:

    allowed_genres = [
        "ужасы",
        "комедия",
        "драма",
        "фантастика",
        "боевик",
        "мелодрама",
        "триллер",
        "детектив",
        "приключения",
        "аниме",
    ]

    def __init__(
        self,
        movie_id: int,
        title: str,
        genres: List[str],
        year: int,
        rating: float,
        director: str = "Не указан",
    ):
        self.__id = movie_id
        self.title = title
        self.genres = genres
        self.director = director
        self.year = year
        self.__rating = rating

    @property
    def id(self):
        return self.__id

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value: float):
        if 0 <= value <= 10:
            self.__rating = round(value, 1)
        else:
            raise ValueError("Рейтинг должен быть от 0 до 10")

    @property
    def genres(self):
        return self.__genres.copy()

    @genres.setter
    def genres(self, genres_list: List[str]):
        invalid_genres = [
            genre for genre in genres_list if genre not in self.allowed_genres
        ]
        if invalid_genres:
            raise ValueError(f"Некорректные жанры: {', '.join(invalid_genres)}")
        self.__genres = genres_list

    def __str__(self) -> str:
        genres_str = ", ".join(self.__genres)
        return f"«{self.title}» ({self.year} | Реж. {self.director} | {genres_str} | Рейтинг: {self.rating}/10)"

    def __repr__(self) -> str:
        return f"id: {self.id}, {self.title!r}"

    def __lt__(self, other: object) -> bool:
        # assert isinstance(other, Movie)
        if not isinstance(other, Movie):
            return NotImplemented
        return self.rating < other.rating

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Movie):
            return NotImplemented
        return self.rating <= other.rating

    def __gt__(self, other: object) -> bool:
        # assert isinstance(other, Movie)
        if not isinstance(other, Movie):
            return NotImplemented
        return self.rating > other.rating

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Movie):
            return NotImplemented
        return self.rating >= other.rating

    def __eq__(self, other: object) -> bool:
        # assert isinstance(other, Movie)
        if not isinstance(other, Movie):
            return NotImplemented
        return self.rating == other.rating

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Movie):
            return NotImplemented
        return self.rating != other.rating
