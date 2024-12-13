import unittest

from jnjserver.entity import EntityType, Entity
from jnjserver.vector import Vector


class TestEntity(unittest.TestCase):
    def setUp(self):
        entity_type = EntityType("test", Vector(10, 10), 6)
        self.entity = Entity(entity_type, Vector(0, 0), 6)

    def test_check_collision(self):
        for x in range(-5, 10):
            for y in range(-5, 10):
                self.assertTrue(self.entity.check_collision(Vector(x, y), Vector(5.1, 5.1)))
        with self.assertRaises(ValueError):
            self.entity.check_collision(123, "asdas")

    def test_walk(self):
        with self.assertRaises(ValueError):
            self.entity.walk(123, "left")
            self.entity.walk("right", "right")
            self.entity.walk(123, 123)

    def test_jump(self):
        with self.assertRaises(ValueError):
            self.entity.jump(Vector(0, 12))
            self.entity.jump("right")

    def test_dict(self):
        expected_dict = {
            "id": self.entity.id,
            "type": self.entity.type.name,
            "position": self.entity.position.dict(),
            "velocity": self.entity.velocity.dict(),
            "is_on_ground": self.entity.is_on_ground,
            "health": self.entity.health,
            "boosts": self.entity.boosts,
            "checkpoints": [c.dict() for c in self.entity.checkpoints],
            "current_checkpoint": self.entity.current_checkpoint.dict()
        }

        self.assertEqual(self.entity.dict(), expected_dict)
