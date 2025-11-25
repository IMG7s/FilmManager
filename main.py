import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.movie_db import MovieDB
from core.entities.movie import Movie


def main():
    print("=== ЗАГРУЗКА БАЗЫ ===")
    db = MovieDB("test_movies.json")
    db.sort_by_rating()
    db.print_all()


if __name__ == "__main__":
    main()
