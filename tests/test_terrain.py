import unittest

from jnjserver.terrain import Terrain
from jnjserver.vector import Vector


class TestTerrain(unittest.TestCase):
    def setUp(self):
        grid = [
            ['', 'bricks', '', '', '', '', '', '', 'crate', ''],
            ['grass', 'bricks', '', '', '', '', '', '', 'crate', ''],
            ['grass', 'bricks', 'dirt', '', '', '', '', 'crate', '', ''],
            ['grass', 'bricks', 'dirt', '', 'bricks', '', '', '', '', ''],
            ['grass', 'bricks', 'bricks', 'bricks', '', '', '', '', '', ''],
            ['', 'bricks', 'bricks', 'bricks', '', '', '', '', '', ''],
            ['', 'bricks', 'dirt', '', '', '', '', '', '', ''],
            ['', 'bricks', 'dirt', '', '', '', 'crate', 'crate', '', ''],
            ['', 'bricks', '', '', '', '', '', '', 'crate', ''],
            ['', 'bricks', '', '', '', '', '', '', '', '']
        ]
        self.terrain = Terrain(grid)

    def test_get_tile(self):
        pos = [[1, 1], [0, 0], [2, 2], [1, 0], [5, 9], [9, 1]]
        tiles = ["bricks", "", "dirt", "grass", "", "bricks"]

        for i in range(6):
            self.assertEqual(self.terrain.get_tile(pos[i][0], pos[i][1]), tiles[i])

        with self.assertRaises(ValueError):
            self.terrain.get_tile("sad", 0)
            self.terrain.get_tile(123, 234.4)
            self.terrain.get_tile(12, 43)

    def test_set_tile(self):
        with self.assertRaises(ValueError):
            self.terrain.set_tile("sad", 0, "234")
            self.terrain.set_tile(123, 234.4, 87)
            self.terrain.set_tile(12, 43, "435")

    def test_remove_tile(self):
        with self.assertRaises(ValueError):
            self.terrain.remove_tile("sad", 0)
            self.terrain.remove_tile(7, 4.4)
            self.terrain.remove_tile(65, 12)

    def test_startup_data(self):
        excpected_startup_data = {
            "grid": self.terrain.grid,
            "width": self.terrain.width,
            "height": self.terrain.height
        }
        self.assertEqual(self.terrain.startup_data(), excpected_startup_data)
