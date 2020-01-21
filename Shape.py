from abc import abstractmethod
from Material import *


class Shape(Point):

    def __init__(self, material: Material):
        """
        Конструктор класса формы с абстрактными методами.

        :param material: материал объекта
        """
        self.material = material

    @abstractmethod
    def does_ray_intersect(self, camera: Point, direction: Point) -> (bool, float):
        """ проверка на пересечение с лучом """

    @abstractmethod
    def normal(self, point: Point) -> Point:
        """ получение нормали """

    def get_color(self, point: Point):
        """ получение цвета в точке """
        return self.material.diffuse

