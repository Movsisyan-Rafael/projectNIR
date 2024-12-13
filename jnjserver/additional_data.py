import json
from jnjserver.entity import Entity
from jnjserver.vector import Vector
from typing import List


class AdditionalData:
    """Дополнительные данные.
    
    Класс, передающий в мир дополнительные данные.

    Attributes:
        checkpoints (dict): Словарь чекпоинтов.
        princess (Vector): Координаты принцессы.
        entities (List[Entity]): Список сущностей.
        
    """

    def __init__(self, checkpoints: dict, princess: Vector, entities: List[Entity]):
        """Дополнительные данные.

        Args:
            checkpoints (dict): Словарь чекпоинтов.
            princess (Vector): Координаты принцессы.
            entities (List[Entity]): Список сущностей.
        """
        self.checkpoints = checkpoints
        self.princess = princess
        self.entities = entities


class AdditionalDataLoader:
    """Загрузчик дополнительных данных из JSON файла.

    Загружает дополнительные данные (чекпоинты, принцессу, сущности) из JSON файла.

    """

    @staticmethod
    def load(json_path: str) -> AdditionalData:
        """Загрузить дополнительные данные из JSON файла.

        Args:
            json_path (str): Путь к JSON файлу.

        Returns:
            AdditionalData: Дополнительные данные.
        """
        json_data = open(json_path)
        data = json.load(json_data)

        checkpoints = {
            "john": [],
            "josh": []
        }

        for checkpoint_data in data["checkpoints"]["john"]:
            checkpoints["john"].append(Vector.from_dict(checkpoint_data))

        for checkpoint_data in data["checkpoints"]["josh"]:
            checkpoints["josh"].append(Vector.from_dict(checkpoint_data))

        princess = Vector.from_dict(data["princess"])

        return AdditionalData(checkpoints, princess, [])
