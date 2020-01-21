import numpy as np


class Point:

    def __init__(self, x=0., y=0., z=0.):
        """
        Конструктор точки.

        :param x: позиция точки по x
        :param y: позиция точки по y
        :param z: позиция точки по z
        """
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y, self.z + p.z)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y, self.z - p.z)

    def __mul__(self, p):
        """ скалярное произведение """
        return self.x * p.x + self.y * p.y + self.z * p.z

    def vector_on_scalar_mult(self, dot):
        """ Вектор на скаляр """
        return Point(self.x * dot, self.y * dot, self.z * dot)

    def vector_mult(self, p):
        """ Вектор * Вектор """
        return Point(self.y * p.z - self.z * p.y, self.z * p.x - self.x * p.z, self.x * p.y - self.y * p.x)

    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def get_length(self):
        return np.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        length = self.get_length()
        if np.abs(length) <= 0.0001:
            length = 1
        return Point(self.x / length, self.y / length, self.z / length)

    def to_color(self):
        """ Приведение цвета к RGB (0..255) """
        red = int(255 * min(1., max(0., self.x)))
        green = int(255 * min(1., max(0., self.y)))
        blue = int(255 * min(1., max(0., self.z)))
        return red, green, blue
