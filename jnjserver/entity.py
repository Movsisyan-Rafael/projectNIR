import random
from math import floor
from jnjserver.vector import Vector
import json
from typing import Union, List


class EntityType:
    """Тип сущности.

    Класс описывающий свойства сущности, единые для всех её экземпляров.

    Attributes:
        name (str): Название.
        size (Vector): Размер.
        max_health (int): Максимальное здоровье.
    """

    def __init__(self, name: str, size: Vector, max_health: int):
        """Тип сущности.

        Args:
            name (str): Название.
            size (Vector): Размер.
            max_health (int): Максимальное здоровье.

        Raises:
            ValueError: Название - строка.
            ValueError: Размер - вектор.
            ValueError: Максимальное здоровье - целое число.
            ValueError: Максимальное здоровье - положительное число.
        """
        if type(name) != str:
            raise ValueError('name should be a string')
        self.name = name

        if type(size) != Vector:
            raise ValueError('size should be a vector')
        self.size = size

        if type(max_health) != int:
            raise ValueError('max_health should be a int')
        elif max_health < 1:
            raise ValueError('max_health should be a positive')
        self.max_health = max_health


class Entity:
    """Сущность.

    Класс описывающий сущность.
    Сущность должна быть добавлена в мир.
    Сущность может быть свзязана с игроком.

    Attributes:
        player_id (str): ID привязанного игрока.
        id (int): ID сущности.
        world (World): Мир, в который добавлена.
        type (EntityType): Тип сущности.
        position (Vector): Вектор позиции.
        velocity (Vector): Вектор скорости.
        is_on_ground (bool): Стоит ли на земле.
        health (int): Здоровье.
        boosts (dict): Словарь с улучшениями и их сроками действия.
        double_jump_ability (bool): Возможность двойного прыжка.
        checkpoints (List[Vector]): Список доступныъх чекпоинтов.
        current_checkpoint (Vector): Текущий чекпоинт.
        is_in_princess (bool): Касается ли принцессы.
        max_speed (Union[int, float]): Максимальная скорость по горизонтали.
    """

    def __init__(self, entity_type: EntityType, position: Vector, health: int):
        """Сущность.

        Args:
            entity_type (EntityType): Тип сущности.
            position (Vector): Позиция.
            health (int): Здоровье.
        """
        self.player_id = None
        self.id = 0
        self.world = None
        self.type = entity_type
        self.position = position
        self.velocity = Vector(0, 0)
        self.is_on_ground = False
        self.health = max(0, min(health, self.type.max_health))
        self.boosts = {
            "jump_boost": 0,
            "speed_boost": 0,
            "double_jump": 0,
            "breaking_through": 0
        }
        self.double_jump_ability = False
        self.checkpoints = []
        self.current_checkpoint = Vector(0, 0)
        self.is_in_princess = False
        self.max_speed = 0.4

    def physics(self):
        """Расчёт физики сущности.

        Считает физику для сущности отталкиваясь от ландшафта мира сущности.
        """
        if self.boosts["speed_boost"]:
            self.max_speed = 0.8
        else:
            self.max_speed = 0.4

        self.velocity.y = min(self.velocity.y + 0.12, 1)
        if self.velocity.x > 0:
            self.velocity.x = max(0.0, self.velocity.x - 0.15)
        elif self.velocity.x < 0:
            self.velocity.x = min(0.0, self.velocity.x + 0.15)

        self.velocity.x = max(-self.max_speed, min(self.velocity.x, self.max_speed))
        colliding_tiles = []

        x_tiles_min = floor(self.position.x) - 1
        x_tiles_max = floor(self.position.x + self.type.size.x) + 2
        y_tiles_min = floor(self.position.y) - 1
        y_tiles_max = floor(self.position.y + self.type.size.y) + 2

        x_tiles_min = max(0, min(x_tiles_min, self.world.terrain.width))
        x_tiles_max = max(0, min(x_tiles_max, self.world.terrain.width))
        y_tiles_min = max(0, min(y_tiles_min, self.world.terrain.height))
        y_tiles_max = max(0, min(y_tiles_max, self.world.terrain.height))

        for x in range(x_tiles_min, x_tiles_max):
            for y in range(y_tiles_min, y_tiles_max):
                if self.world.tileset.get(self.world.terrain.get_tile(x, y)).solid:
                    colliding_tiles.append(Vector(x, y))

        self.is_on_ground = False

        x_min = self.velocity.x
        y_min = self.velocity.y

        for tile in colliding_tiles:
            if self.position.x + self.type.size.x + x_min > tile.x and self.position.x + x_min < tile.x + 1 and self.position.y + self.type.size.y > tile.y and self.position.y < tile.y + 1:
                if x_min > 0:
                    x_min = min(x_min, tile.x - (self.position.x + self.type.size.x))
                elif x_min < 0:
                    x_min = max(x_min, tile.x + 1 - self.position.x)
                self.velocity.x = 0

            elif self.position.x + self.type.size.x > tile.x and self.position.x < tile.x + 1 and self.position.y + self.type.size.y + y_min > tile.y and self.position.y + y_min < tile.y + 1:
                if y_min > 0:
                    y_min = min(y_min, tile.y - (self.position.y + self.type.size.y))
                    self.is_on_ground = True
                    self.double_jump_ability = True
                elif y_min < 0:
                    y_min = max(y_min, tile.y + 1 - self.position.y)
                    self.hit_ceil(tile)
                self.velocity.y = 0

        self.position.x += x_min
        self.position.y += y_min

        if self.position.y > self.world.terrain.height:
            self.die()

        self.check_princess()

    def check_collision(self, position: Vector, size: Vector) -> bool:
        """Проверка коллизии с объектом.

        Проверяет пересекается ли сущность с объектом имеющем предоставленные коорлинаты и размер.
        Возвращает логическое значение.

        Args:
            position (Vector): Позиция объекта.
            size (Vector): Размер объекта.

        Raises:
            ValueError: Позиция объекта - вектор.
            ValueError: Размер объекта - вектор.

        Returns:
            bool: Состояние коллизии.
        """
        if type(position) != Vector:
            raise ValueError('position should be a vector')

        if type(size) != Vector:
            raise ValueError('size should be a vector')

        x_collision = self.position.x + self.type.size.x > position.x and self.position.x < position.x + size.x
        y_collision = self.position.y + self.type.size.y > position.y and self.position.y < position.y + size.y
        return x_collision and y_collision

    def check_princess(self):
        """Проверка коллизии с принцессой.

        Проверяет пересекается ли сущность с принцессой.
        Возвращает логическое значение.
        """
        self.is_in_princess = self.check_collision(self.world.princess, Vector(1, 2))

    def hit_ceil(self, tile: Vector):
        """Обработать удар об потолок.
        
        Метод, вызывающийся при ударе головй об блок снизу вверх.
        Ломает ящик или блок улучшения.
        При поломке блока улучшения даёт случайное улучшение.
        При действии улучшения "Пробитие" ломает любой блок.

        Args:
            tile (Vector): Координаты плитки, об которую сущность ударилась.
        """
        if self.world.terrain.get_tile(tile.x, tile.y) == "upgrade":
            available_boosts = [boost for boost in self.boosts.keys() if not self.boosts[boost]]
            if available_boosts:
                boost = random.choice(available_boosts)
                self.boosts[boost] = random.randint(450, 600)
        if self.boosts["breaking_through"] or self.world.terrain.get_tile(tile.x, tile.y) in ["crate", "upgrade"]:
            self.world.terrain.set_tile(tile.x, tile.y, "")

    def walk(self, direction: str, walking_velocity: Union[int, float]):
        """Ходить.

        Передача сущности предоставленной скорости по горизонтали в предоставленном направлении.

        При направлении "right" с скорости сущности добавляется предоставленная скорость.
        При навправлении "left" из скорости сущности она вычитается.

        Args:
            direction (str): Направление ("left", "right").
            walking_velocity (Union[int, float]): Скорость ходьбы.

        Raises:
            ValueError: Направление - строка.
            ValueError: Скорость ходьбы - число.
        """
        if type(direction) != str:
            raise ValueError('direction should be a string')

        if type(walking_velocity) not in [int, float]:
            raise ValueError('walking_velocity should be a number')

        if direction == "left":
            self.velocity.x -= walking_velocity
        elif direction == "right":
            self.velocity.x += walking_velocity

    def jump(self, jump_velocity: Union[int, float]):
        """Подпрыгнуть.

        Прыжок с предоставленной скоростью.
        Из скорости сущности по вертикали вычитается предоставленная скорость.

        Args:
            jump_velocity (Union[int, float]): Скорость прыжка.

        Raises:
            ValueError: Скорость прыжка - число.
        """
        if type(jump_velocity) not in [int, float]:
            raise ValueError('jump_velocity should be a number')

        if self.boosts["jump_boost"]:
            jump_velocity += 0.2
        if self.is_on_ground:
            self.velocity.y -= jump_velocity
        elif self.double_jump_ability and self.boosts["double_jump"]:
            self.velocity.y -= jump_velocity
            self.double_jump_ability = False

    def die(self):
        """Умереть.

        Отнимает одно здоровье у сущности и перемещает её на координаты текущего чекпоинта.
        """
        self.position = self.current_checkpoint.clone()
        for bk in self.boosts.keys():
            self.boosts[bk] = 0
        self.health -= 1

    def update_boosts(self):
        """Обновить состояние усилений.

        Уменьшает оставшееся время работы усилений.
        """
        for boost in self.boosts.keys():
            self.boosts[boost] = max(self.boosts[boost] - 1, 0)

    def update_checkpoint(self):
        """Обновить чекпоинт.

        Проверяет пересечение с чекпоинтами и меняет чекпоинт на текущий, если сущность пересекается с ним.
        """
        for checkpoint in self.checkpoints:
            if self.check_collision(checkpoint, Vector(1, 1)):
                self.current_checkpoint = checkpoint

    def update(self):
        """Обновить всё.

        Обновляет состояние сущности.        
        """
        self.physics()
        self.update_boosts()
        self.update_checkpoint()

    def dict(self) -> dict:
        """Создать словарь содержащий свойства сущности.

        Возвращает словарь содержащий свойства сущности.
        Нужно для отправки данных клиенту.

        Returns:
            dict: Словарь содержащий свойства сущности.
        """
        return {
            "id": self.id,
            "type": self.type.name,
            "position": self.position.dict(),
            "velocity": self.velocity.dict(),
            "is_on_ground": self.is_on_ground,
            "health": self.health,
            "boosts": self.boosts,
            "checkpoints": [c.dict() for c in self.checkpoints],
            "current_checkpoint": self.current_checkpoint.dict()
        }


class EntitySet:
    """Сет типов сущностей.

    Класс для получения типов сущностей по именам.

    Attributes:
        entities_types (str): словарь типов сущностей. 
    """

    def __init__(self, entities_types: dict):
        """Сет типов сущностей

        Класс для получения типов сущностей по именам.

        Args:
            entities_types (dict): Словарь типов сущностей.
        """
        self.entities_types = entities_types

    def get(self, entity_type: str) -> EntityType:
        """Получить тип сущности по названию.

        Возвращает тип сущности по названию.

        Args:
            entity_type (str): Название типа сущности.

        Returns:
            EntityType: Тип сущности.
        """
        return self.entities_types[entity_type]


class EntitySetLoader:
    """Загрузчик типов сущностей из JSON файла.

    Загружает типы сущностей из JSON файла.
    """

    @staticmethod
    def load(json_path: str) -> EntitySet:
        """Загрузть типы сущностей из JSON файла.

        Args:
            json_path (str): Путь к JSON файлу.

        Returns:
            EntitySet: Сет типов сущностей.
        """
        json_data = open(json_path)
        data = json.load(json_data)
        entities_types = {}

        for entity_type_data in data:
            name = entity_type_data["name"]
            size = Vector.from_dict(entity_type_data["size"])
            max_health = entity_type_data["max_health"]
            entity_type = EntityType(name, size, max_health)
            entities_types[name] = entity_type
        return EntitySet(entities_types)
