from Shape import *


class Side(Shape):

    def __init__(self, points: list, material: Material, norm: Point, eps: float = 0.0001):
        """
        Конструктор стороны куба.

        :param points: расположение стороны куба. Список из четырёх точек
        :param material: материал стороны
        :param norm: нормаль к стороне
        :param eps:
        """
        self.eps = eps
        self.points = list()
        for p in points:
            self.points.append(Point(p.x, p.y, p.z))
        self.material = material
        self.norm = Point(norm.x, norm.y, norm.z)

    def ray_intersects_triangle(self, camera: Point, direction: Point,
                                p0: Point, p1: Point, p2: Point) -> (bool, float):
        intersect = -1.
        edge1: Point = p1 - p0
        edge2: Point = p2 - p0
        h: Point = direction.vector_mult(edge2)
        a: float = edge1 * h

        if -self.eps < a < self.eps:
            return False, intersect     # Этот луч параллелен этому треугольнику.

        f: float = 1. / a

        s: Point = camera - p0
        u: float = s * h * f
        if u < 0 or u > 1:
            return False, intersect

        q: Point = s.vector_mult(edge1)
        v: float = direction * q * f
        if v < 0 or v + u > 1:
            return False, intersect

        # На этом этапе мы можем вычислить t, чтобы узнать, где находится точка пересечения на линии.
        t: float = edge2 * q * f

        if t > self.eps:
            intersect = t
            return True, intersect
        else:   # Это означает, что есть пересечение линий, но не пересечение лучей.
            return False, intersect

    def does_ray_intersect(self, camera: Point, direction: Point) -> (bool, float):
        """ Пересекает ли луч сторону """
        intersect = np.inf
        f = self.ray_intersects_triangle(camera, direction, self.points[0], self.points[1], self.points[3])
        f2 = self.ray_intersects_triangle(camera, direction, self.points[1], self.points[2], self.points[3])
        if f[0] and (intersect == np.inf or f[1] < intersect):
            intersect = f[1]
        elif f2[0] and (intersect == np.inf or f[1] < intersect):
            intersect = f2[1]

        if intersect != np.inf:
            return True, intersect
        return False, intersect

    def normal(self, point: Point) -> Point:
        """ Нормаль к стороне """
        return self.norm
