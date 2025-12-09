import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities.user import User
from utils.user_db import UserDB


if __name__ == "__main__":
    user = User("Alex", "secure_password")
    user.addGenre(["боек", "драма"])

    user_dict = user.to_dict()
    print("Словарь:", user_dict)

    user_from_dict = User.from_dict(user_dict)
    print("Восстановленный пользователь:")
    print(user_from_dict)

    db = UserDB("test_users.json")
    db.add_user(user)
    db.save()
