from Point import *


class Light:

    def __init__(self, intensity: float, position: Point):
        """
        Конструктор света.

        :param intensity: интенсивность источника света
        :param position: позиция источника света
        """
        self.intensity = intensity
        self.position = Point(position.x, position.y, position.z)
