class ServerUpdatesHandler:
    """Обработчик обновлений.

    Обрабатывает принятые с сервера данные обновлений текущей игры.

    Attributes:
        grid (List[List[str]]): Двумерный список плиток.
        terrain_width (int): Ширина ландшафта в плитках.
        terrain_height (int): Высота ландшафта в плитках.
        entities (dict): Словарь сущностей.
        checkpoints (dict): Словарь чекпоинтов.
        princess (dict): Словарь координат принцессы.
        player_entity (dict): Словарь сущности игрока.
        id: (str): ID игрока ("john", "josh").
    """

    def __init__(self, startup_data: dict):
        """Обработчик обновлений

        Обрабатывает принятые с сервера данные обновлений текущей игры.

        Args:
            startup_data (dict): Словарь начальных данных.
        """
        self.grid = startup_data["terrain"]["grid"]
        self.terrain_width = startup_data["terrain"]["width"]
        self.terrain_height = startup_data["terrain"]["height"]
        self.entities = startup_data["entities"]
        self.checkpoints = startup_data["checkpoints"]
        self.princess = startup_data["princess"]
        self.player_entity = startup_data["player_entity"]
        self.id = startup_data["player_id"]

    def process_update(self, update_data: dict):
        """Обработать обновление

        Обрабатывает обновление, присланное с сервера.

        Args:
            update_data (dict): Словарь с данными обновления.
        """
        self.entities = update_data["entities"]

        self.player_entity = update_data["player_entity"]
        for grid_update in update_data["actions"]["terrain"]:
            self.grid[grid_update["x"]][grid_update["y"]] = grid_update["tile"]
