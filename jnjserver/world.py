from jnjserver.entity import EntitySet, Entity
from jnjserver.additional_data import AdditionalData
from jnjserver.terrain import TileSet, Terrain


class World:
    """Мир (интерфейс взаимодействия сервера с игровой логикой).

    Класс, свзязывающий все состовляющие мира игры (плитки, ландшафт, сущности, дополнительыне данные).
    Объединяет внутриигровую логику и создаёт интерфейс взаимодействия сервера с миром игры.

    Attributes:
        tileset (TileSet): Сет плиток.
        entityset (EntitySet): Сет типов сущностей.
        terrain (Terrain): Ландшафт.
        entities (List[Entity]): Список сущностей.
        current_entity_id (int): ID, присваивающийся добавленной сущности (после добавления обновляется).
        john_entity (Entity): Сущность Джона.
        josh_entity (Entity): Сущность Джоша.
        princess (Vector): Координаты принцессы.
        checkpoints (dict): Словарь чекпоинтов.

    """

    def __init__(self, tileset: TileSet, entityset: EntitySet, terrain: Terrain, additional_data: AdditionalData):
        """Мир (интерфейс взаимодействия сервера с игровой логикой).

        Args:
            tileset (TileSet): Сет плиток.
            entityset (EntitySet): Сет типов сущностей.
            terrain (Terrain): Ландшафт.
            additional_data (AdditionalData): Дополнительные данные.
        """
        self.tileset = tileset
        self.entityset = entityset
        self.terrain = terrain
        self.entities = []
        self.current_entity_id = 0
        self.john_entity = None
        self.josh_entity = None

        self.princess = additional_data.princess
        self.checkpoints = additional_data.checkpoints
        for entity in additional_data.entities:
            self.add_entity(entity)

    def add_entity(self, entity: Entity):
        """Добавить сущность.

        Добавляет сущность в мир, сущности присваевается свой уникальный ID и передаётся сслыка на мир.
        
        Args:
            entity (Entity): Сущность.
        """
        entity.id = self.current_entity_id
        entity.world = self

        if entity.player_id == "john":
            self.john_entity = entity
        elif entity.player_id == "josh":
            self.josh_entity = entity

        self.current_entity_id += 1
        self.entities.append(entity)

    def update_entities(self):
        """Обновить сущности.

        Обновляет состояние всех сущностей этого мира. 
        """
        for entity in self.entities:
            entity.update()

    def update(self):
        """Обновить всё.
        
        Обновляет состояние мира.
        """
        self.update_entities()

    def startup_data(self) -> dict:
        """Получить начальные данные

        Возвращает словарь с данными нужными клиенту для начала работы.

        Returns:
            dict: Словарь с начальными данные.
        """
        startup_data = {
            "type": "startup",
            "terrain": self.terrain.startup_data(),
            "entities": self.extract_entities_updates()
        }
        startup_data.update(self.additional_startup_data())
        return startup_data

    def extract_entities_updates(self) -> dict:
        """Извлечь обновления сущностей

        Возвращает обновлённые данные о сущностях мира в виде словаря.

        Returns:
            dict: Словарь обновлейний сущностей.
        """
        entities_updates = {}
        for entity in self.entities:
            entities_updates[str(entity.id)] = entity.dict()
        return entities_updates

    def additional_startup_data(self) -> dict:
        """Получить дополнительные начальные данные.

        Возвращает словарь с дополнительными данными, нужными для начала работы клиента.

        Returns:
            dict: Словарь дополнительных начальных данных.
        """
        return {
            "princess": self.princess.dict(),
            "checkpoints": {
                "john": [checkpoint.dict() for checkpoint in self.checkpoints["john"]],
                "josh": [checkpoint.dict() for checkpoint in self.checkpoints["josh"]]
            }
        }

    def extract_updates(self) -> dict:
        """Извлечь обновления.

        Возвращает словарь со всеми обновлениями мира, произошедшими с предыдущего получения обновления.

        Returns:
            dict: Обновления.
        """
        terrain_updates = self.terrain.extract_updates()
        entities_updates = self.extract_entities_updates()

        return {
            "type": "update",
            "actions": {
                "terrain": terrain_updates
            },
            "entities": entities_updates
        }
