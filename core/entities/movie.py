class Movie:
    def __init__(
        self,
        movie_id: int,
        title: str,
        genres: list[str],
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

    def __str__(self) -> str:
        return f"«{self.title}» ({self.year} | Реж. {self.director} | {[_ for _ in self.genres]} | Рейтинг: {self.rating}/10)"

    def __repr__(self) -> str:
        return f"id: {self.id}, {self.title!r}"

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, Movie)
        return self.rating < other.rating

    def __gt__(self, other: object) -> bool:
        assert isinstance(other, Movie)
        return self.rating > other.rating
