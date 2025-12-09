import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
import json
from typing import Dict, List, Optional
from core.entities.user import User


class UserDB:
    """
    Хранилище User'ов
    Работает с объектами User
    """

    def __init__(self, db_path: str) -> None:
        self._db_path = Path(db_path).absolute()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self.db: List[User] = []  # список всех пользователей
        self.by_id: Dict[int, User] = {}  # быстрый доступ по ID

        self.load_db()

    def load_db(self) -> None:
        """
        Загрузка JSON и преобразование словаря в User объект.
        """
        raw_data = []

        if self._db_path.exists():
            try:
                with open(self._db_path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Ошибка в JSON файле {self._db_path}: {e}")
                print("Создаю пустую базу.")
                raw_data = []
        else:
            print(f"База не найдена - создаю новую: {self._db_path}")

        # Очищаем текущие данные
        self.db.clear()
        self.by_id.clear()

        # Загружаем данные
        loaded_count = 0
        for item in raw_data:
            try:
                user = User.from_dict(item)
                self._add_to_memory(user)
                loaded_count += 1
            except Exception as e:
                print(f"Пропущена запись: {item} ({e})")

        print(
            f"База загружена, пользователей: {len(self.db)} (успешно загружено: {loaded_count})"
        )

    def save(self) -> None:
        """Сохраняет всех пользователей в JSON файл."""
        # Преобразуем всех пользователей в словари
        data = [user.to_dict() for user in self.db]

        try:
            with open(self._db_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"База сохранена в {self._db_path}")
        except Exception as e:
            print(f"Ошибка при сохранении базы: {e}")

    def _add_to_memory(self, user: User) -> None:
        """Добавляет пользователя в обе структуры данных."""
        # Автоматически генерируем ID если он не задан
        if user.id == 0:
            new_id = max(self.by_id.keys(), default=0) + 1
            user.id = new_id

        # Проверяем уникальность ID
        if user.id in self.by_id:
            print(f"Предупреждение: пользователь с ID {user.id} уже существует")
            # Удаляем старого пользователя с таким же ID
            existing_user = self.by_id[user.id]
            self.db.remove(existing_user)

        self.db.append(user)
        self.by_id[user.id] = user

    def add_user(self, user: User) -> None:
        """Публичный метод для добавления пользователя."""
        self._add_to_memory(user)

    def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        return self.by_id.get(user_id)

    def __len__(self) -> int:
        """Количество пользователей."""
        return len(self.db)

    def __str__(self) -> str:
        return f"UserDB(users={len(self)}, path={self._db_path})"
