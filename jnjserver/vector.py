from typing import Union


class Vector:
    """Вектор

    Класс реализующий векторы.

    Attributes:
        x (Union[int, float]): Координата x
        y (Union[int, float]): Координата y
    """

    def __init__(self, x: Union[int, float], y: Union[int, float]):
        """Новый вектор из двух координат.

        Args:
            x Union[int, float]: Координата x.
            y Union[int, float]: Координата y.
        """
        self.x = x
        self.y = y

    @staticmethod
    def from_dict(dict_vector):
        """Новый вектор из словаря, содержащего координаты.

        Возвращает вектор с коорлинатами, записанными в предоставленном словаре.

        Args:
            dict_vector (dict): Словарь, содержащий координаты.

        Returns:
            Vector: Вектор из словаря, содержащего координаты.
        """
        return Vector(dict_vector["x"], dict_vector["y"])

    def add(self, vector):
        """Прибавить к вектору вектор.

        Прибавляет к вектору предоставленный вектор.

        Args:
            vector (Vector): Вектор, который будет прибавлен.
        """
        self.x += vector.x
        self.y += vector.y

    def sub(self, vector):
        """Вычесть из вектора вектор.

        Вычитает из вектора предоставленный вектор.

        Args:
            vector (Vector): Вектор, который будет вычтен.
        """
        self.x -= vector.x
        self.y -= vector.x

    def dict(self):
        """Создать словарь, содержащий координаты вектора.

        Возвращает словарь, содержащий координаты вектора

        Returns:
            dict: Словарь, содержащий координаты вектора.
        """
        return {
            "x": self.x,
            "y": self.y
        }

    def clone(self):
        """Клонировать вектор.

        Возвращает клон вектора.

        Returns:
            Vector: Клон этого вектора.
        """
        return Vector(self.x, self.y)
