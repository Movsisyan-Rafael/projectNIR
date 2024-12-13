import json
from typing import List


class Tile:
    def __init__(self, name: str, solid: bool):
        """Плитка

        Args:
            name (str): Название плитки
            solid (bool): Твёрдость плитки (True - твёрдая, False - не твёрдая)
        """
        self.name = name
        self.solid = solid


class TileSetLoader:
    @staticmethod
    def load(json_path: str):
        json_data = open(json_path)
        data = json.load(json_data)
        tiles = {}
        for tile_data in data:
            name = tile_data["name"]
            solid = tile_data["solid"]
            tile_type = Tile(name, solid)
            tiles[name] = tile_type
        return TileSet(tiles)


class TileSet:
    def __init__(self, tiles: dict):
        """Сет плиток.

        Args:
            tiles (dict): Словарь плиток.
        """
        self.tiles = tiles

    def get(self, tile: str):
        """Получить плитку по названию.

        Args:
            tile (str): Название плитки.

        Returns:
            Tile: Плитка.
        """
        return self.tiles[tile]


class Terrain:
    def __init__(self, grid: List[List[str]]):
        """Ландшафт.

        Args:
            grid (List[List[str]]): Двумерный массив названий плиток.
        """
        self.grid = grid
        self.width = len(grid)
        self.height = len(grid[0])
        self.updates = []

    def get_tile(self, x: int, y: int) -> str:
        """Получить название плитки на координатах.

        Args:
            x (int): Координата x.
            y (int): Координата y.

        Raises:
            ValueError: Координата x - целое число.
            ValueError: Координата y - целое число.
            ValueError: Нет плитки на координатах.

        Returns:
            str: Название плитки.
        """
        if type(x) != int:
            raise ValueError('x should be a int')

        if type(y) != int:
            raise ValueError('y should be a int')

        if x > self.width or y > self.height:
            raise ValueError(f'There is no tile with x: {x}, y: {y}')

        return self.grid[x][y]

    def set_tile(self, x: int, y: int, tile: str):
        """Задать название плитки на координатах.

        Args:
            x (int): Координата x.
            y (int): Координата y.
            tile (str): Название плитки.

        Raises:
            ValueError: Координата x - целое число.
            ValueError: Координата y - целое число.
            ValueError: Название - строка.
            ValueError: Нет плитки на координатах.
        """
        if type(x) != int:
            raise ValueError('x should be a int')

        if type(y) != int:
            raise ValueError('y should be a int')

        if type(tile) != str:
            raise ValueError('tile should be a string')

        if x > self.width or y > self.height:
            raise ValueError(f'There is no tile with x: {x}, y: {y}')

        self.grid[x][y] = tile
        terrain_update = {
            "x": x,
            "y": y,
            "tile": tile
        }
        self.updates.append(terrain_update)

    def remove_tile(self, x: int, y: int):
        """Назначить пустую плитку на координатах.

        Args:
            x (int): Координата x.
            y (int): Координата y.

        Raises:
            ValueError: Координата x - целое число.
            ValueError: Координата y - целое число.
            ValueError: Нет плитки на координатах.
        """
        if type(x) != int:
            raise ValueError('x should be a int')

        if type(y) != int:
            raise ValueError('y should be a int')

        if x > self.width or y > self.height:
            raise ValueError(f'There is no tile with x: {x}, y: {y}')

        self.grid[x][y] = ""
        terrain_update = {
            "x": x,
            "y": y,
            "tile": ""
        }
        self.updates.append(terrain_update)

    def extract_updates(self) -> List[dict]:
        """Извлечь обновления ландшафта.

        Returns:
            List[dict]: Список обновлений ландшафта.
        """
        updates_to_extract = self.updates
        self.updates = []
        return updates_to_extract

    def startup_data(self) -> dict:
        """Получить данные о всём ландшафте.

        Returns:
            dict: Данные о всём ландшафте.
        """
        return {
            "grid": self.grid,
            "width": self.width,
            "height": self.height
        }


class TerrainLoader:
    @staticmethod
    def load(csv_path: str):
        """Загрузить ландшафт из CSV файла.

        Args:
            csv_path (str): Путь к CSV файлу.

        Returns:
            Terrain: Ландшафт.
        """
        grid_temp = []

        for row in open(csv_path):
            grid_temp.append(row[:-1].split(';'))

        grid = []

        for y in range(len(grid_temp)):
            for x in range(len(grid_temp[y])):
                # Поменять столбцы и строки
                if y == 0:
                    if grid_temp[y][x] != 'air':
                        grid.append([grid_temp[y][x]])
                    else:
                        grid.append([''])
                else:
                    if grid_temp[y][x] != 'air':
                        grid[x].append(grid_temp[y][x])
                    else:
                        grid[x].append('')
        return Terrain(grid)
