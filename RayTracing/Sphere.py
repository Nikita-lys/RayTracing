from RayTracing.Shape import *


class Sphere(Shape):

    def __init__(self, center: Point, radius: float, material: Material, eps: float = 0.0001):
        """
        Конструток сферы.

        :param center: координаты центра
        :param radius: радиус
        :param material: материал сферы
        :param eps:
        """
        self.eps = eps
        self.center = center
        self.radius = radius
        self.material = material

    def does_ray_intersect(self, camera: Point, direction: Point):
        """ Пересекает ли луч сферу """
        # определяет предполагаемое положение пересечения (начало луча - центр сферы)
        intersection_point = camera - self.center

        # вычисляет дискриминант
        b = intersection_point * direction
        c = intersection_point * intersection_point - self.radius * self.radius
        discriminant = b * b - c

        # если дискриминант меньше нуля, то пересечения с лучом нет и t - бесконечность
        if discriminant < self.eps:
            res = np.inf
            return False, res

        # вычисляет корень уравнения
        res = -b - np.sqrt(discriminant)

        # если корень меньше нуля, то пересечения с лучом нет
        if res < self.eps:
            res = -b + np.sqrt(discriminant)

        return res > self.eps, res

    def normal(self, point: Point):
        """ Нормаль к сфере - вектор между точкой и центром сферы """
        return (point - self.center).normalize()
