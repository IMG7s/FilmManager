import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.entities.movie import Movie


# a = Movie(0, "Piska", ["Драма", "Какашка"], 2025, 6.7, "Абобик")
# b = Movie(0, "Pisun", ["Какашка"], 2025, 6.7, "OCHKO")

# print(a.id)
# print(f"Рейтинг до изм | {a.rating}")
# a.rating = 2
# print(f"Рейтинг после изм | {a.rating}")


# print(str(a))
# print(repr(a))
# print(a < b)
# print(a == b)

# try:
#     movie = Movie(
#         movie_id=1,
#         title="Фильм ужасов",
#         genres=["ужасы"],
#         year=2025,
#         rating=7.5,
#     )
# except ValueError as e:
#     print(e)

# # movie.genres = ["комедия", "дрма"]

# # print(movie.genres)
# print(movie)


# data = {
#     "id": 1,
#     "title": "Интерстеллар",
#     "genres": ["фантастика", "драма"],
#     "year": 2014,
#     "rating": 22.0,
#     "director": "Кристофер Нолан",
# }

# movie = Movie.from_dict(data)

# print(movie)
# print(movie.to_dict())
