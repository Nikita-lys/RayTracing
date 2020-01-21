from Point import *


class Material:

    def __init__(self, refractive: float, diffuse: Point, specular: float, albedo: list):
        """
        Конструктор материала объекта.

        :param refractive: показатель преломления
        :param diffuse: показатель рассеянности
        :param specular: показатель отражаемости
        :param albedo: коэффициент смешивания (характеристика отражательных свойств поверхности)
        """
        self.refractive = refractive
        self.diffuse = diffuse
        self.specular = specular
        self.albedo = albedo
