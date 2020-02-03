from RayTracing.Sphere import *
from RayTracing.Side import *
from RayTracing.Light import *


eps = 0.0001


class ColorOfPicture:
    """ Посчёт цвета в кадждом пикселе выходной картинки. """

    def __init__(self, camera=Point(), width=0, height=0, shapes=list(), lights=list(), buffer=list()):
        self.camera: Point = camera
        self.width: int = width
        self.height: int = height
        self.shapes: list = shapes

        self.bitmap = list()

        # источники света
        self.lights: list = lights

        self.buffer: list = buffer
        self.x: list = list()
        self.y: list = list()

        self.size: int = max(self.width, self.height)

        for i in range(self.width * self.height):
            self.x.append(float(i % self.width) / self.size - 0.5)
            self.y.append(0.5 - (float(i) / self.width) / self.size)

        self.build_scene()
        self.run()

    # Задаём используемые материалы
    green = Material(refractive=1.0,
                     albedo=[1, 0.5],
                     diffuse=Point(0, 0.3, 0),
                     specular=10)

    red = Material(refractive=1.0,
                   albedo=[1, 0.5],
                   diffuse=Point(1, 0, 0),
                   specular=10)

    darkblue = Material(refractive=1.0,
                        albedo=[1, 0.5],
                        diffuse=Point(0, 0, 1),
                        specular=10)

    yellow = Material(refractive=1.0,
                      albedo=[1, 0.5],
                      diffuse=Point(1, 1, 0),
                      specular=10)

    blue = Material(refractive=1.0,
                    albedo=[1, 0.5],
                    diffuse=Point(0.5, 0.3, 1),
                    specular=10)

    pink = Material(refractive=1.0,
                    albedo=[1, 0.5],
                    diffuse=Point(1, 0, 1),
                    specular=10)

    background_color = Point(1, 1, 1)

    def build_scene(self):
        """ Создаём комнату с объектами """
        self.shapes = [
            Side([Point(-0.5, -0.5, 4.5),
                  Point(-0.5, 0.5, 4.5),
                  Point(-0.5, 0.5, -4.5),
                  Point(-0.5, -0.5, -4.5)],
                 material=self.red,
                 norm=Point(1, 0, 0)),

            Side([Point(0.5, -0.5, 4.5),
                  Point(0.5, 0.5, 4.5),
                  Point(0.5, 0.5, -4.5),
                  Point(0.5, -0.5, -4.5)],
                 material=self.darkblue,
                 norm=Point(-1, 0, 0)),

            Side([Point(0.5, -0.5, 4.5),
                  Point(-0.5, -0.5, 4.5),
                  Point(-0.5, -0.5, -4.5),
                  Point(0.5, -0.5, -4.5)],
                 material=self.green,
                 norm=Point(0, 1, 0)),

            Side([Point(0.5, 0.5, 4.5),
                  Point(-0.5, 0.5, 4.5),
                  Point(-0.5, 0.5, -4.5),
                  Point(0.5, 0.5, -4.5)],
                 material=self.yellow,
                 norm=Point(0, -1, 0)),

            Side([Point(0.5, 0.5, 2),
                  Point(-0.5, 0.5, 2),
                  Point(-0.5, -0.5, 2),
                  Point(0.5, -0.5, 2)],
                 material=self.blue,
                 norm=Point(0, 0, -1)),

            Side([Point(0.5, 0.5, 0),
                  Point(-0.5, 0.5, 0),
                  Point(-0.5, -0.5, 0),
                  Point(0.5, -0.5, 0)],
                 material=self.pink,
                 norm=Point(0, 0, 1)),

            Sphere(Point(0.2, -0.3, 1.2), 0.07, self.red),
            Sphere(Point(0.1, 0.2, 1.6), 0.15, self.green),

            Side([Point(-0.1, -0.2, 1.6),
                  Point(-0.3, -0.2, 1.6),
                  Point(-0.3, -0.2, 1.4),
                  Point(-0.1, -0.2, 1.4)],
                 material=self.yellow,
                 norm=Point(0, -1, 0)),

            Side([Point(-0.1, -0.2, 1.4),
                  Point(-0.1, -0.0, 1.4),
                  Point(-0.1, -0.0, 1.6),
                  Point(-0.1, -0.2, 1.6)],
                 material=self.yellow,
                 norm=Point(1, 0, 0)),

            Side([Point(-0.1, -0.2, 1.6),
                  Point(-0.3, -0.2, 1.6),
                  Point(-0.3, -0.0, 1.6),
                  Point(-0.1, -0.0, 1.6)],
                 material=self.yellow,
                 norm=Point(0, 0, 1)),

            Side([Point(-0.3, -0.2, 1.6),
                  Point(-0.3, -0.2, 1.4),
                  Point(-0.3, -0.0, 1.4),
                  Point(-0.3, -0.0, 1.6)],
                 material=self.yellow,
                 norm=Point(-1, 0, 0)),

            Side([Point(-0.1, -0.2, 1.4),
                  Point(-0.3, -0.2, 1.4),
                  Point(-0.3, -0.0, 1.4),
                  Point(-0.1, -0.0, 1.4)],
                 material=self.yellow,
                 norm=Point(0, 0, -1)),

            Side([Point(-0.1, -0.0, 1.4),
                  Point(-0.3, -0.0, 1.4),
                  Point(-0.3, -0.0, 1.6),
                  Point(-0.1, -0.0, 1.6)],
                 material=self.yellow,
                 norm=Point(0, 1, 0))
        ]

        self.lights = [Light(intensity=0.8, position=Point(0, 0.4, 1)),
                       Light(intensity=0.3, position=Point(0.4, 0.1, 1))]

    def closest_intersection(self, camera: Point, direction: Point, min_dist: float = eps, max_dist: float = np.inf) \
            -> (Shape, float):
        """
        Находит ближайший объект, с которым пересекается луч.

        :param camera: Позиция камеры, откуда летит луч.
        :param direction: Позиция пикселя, куда летит луч.
        :param min_dist:
        :param max_dist:
        :return: (Ближайший объект, дистанция до ближайшего объекта)
        """

        # предполагает, что нет пересечения
        closest_distance: float = np.inf
        closest_shape: Shape = None

        for shape in self.shapes:
            t = shape.does_ray_intersect(camera=camera, direction=direction)
            if not t[0]:
                continue
            # если удовлетворяет параметрам луча (tmin, tmax) и меньше ближайшего
            # расстония - обновляет ближайшее расстоние и запоминает ближайшую фигуру
            if (t[1] < min_dist) or (t[1] > max_dist) or (t[1] >= closest_distance):
                continue
            closest_distance = t[1]
            closest_shape = shape

        return closest_shape, closest_distance

    def have_intersection(self, camera: Point, direction: Point, min_dist: float = eps, max_dist: float = np.inf) \
            -> bool:
        """
        Проверяет, есть ли пересечение с объектом.

        :param camera: Позиция камеры, откуда летит луч.
        :param direction: Позиция пикселя, куда летит луч.
        :param min_dist:
        :param max_dist:
        :return: True если есть, False если нет
        """
        for shape in self.shapes:
            t = shape.does_ray_intersect(camera=camera, direction=direction)
            if t[0] and min_dist <= t[1] <= max_dist:
                return True
        return False

    def lighting(self, point: Point, normal: Point, direction: Point, material: Material) -> (float, float):
        """
        Вычисляет освещение источников света

        :param point: Точка пересечения луча с объектом.
        :param normal: Нормаль в точке пересечения луча с объектом.
        :param direction: Позиция пикселя, куда летит луч.
        :param material: материал ближайшего объекта.
        :return: (рассеяние, отражаемость)
        """
        diffuse: float = 0.
        specular: float = 0.

        for light in self.lights:
            # вычисляет вектор направления луча от источника света
            light_direction: Point = light.position - point
            # максимальное расстояние
            max_dist: float = light_direction.get_length()
            light_direction = light_direction.normalize()

            # проверяет на нахождение в тени и переходит к следующему источнику
            if self.have_intersection(camera=point, direction=light_direction, max_dist=max_dist):
                continue

            # вычисляет косинус угла между источником света и нормалью
            light_cos: float = light_direction * normal
            # увеличение показателя рассеянности
            diffuse += light_cos * light.intensity

            # вычисляет косинус угла между отражённым лучём и направлением луча
            specular_cos: float = (light_direction - normal.vector_on_scalar_mult(light_cos * 2)) * direction
            # увеличение показателя отражаемости
            specular += np.power(specular_cos, material.specular) * light.intensity

        diffuse *= material.albedo[0]
        specular *= material.albedo[1]

        return diffuse, specular

    def ray(self, camera: Point, direction: Point) -> Point:
        """
        Посчёт выходного цвета.

        :param camera: Позиция камеры, откуда летит луч.
        :param direction: Позиция пикселя, куда летит луч.
        :return: Цвет.
        """
        # находит ближайший объект, с которым пересекается луч
        closest_shape, closest_dist = self.closest_intersection(camera=camera, direction=direction)

        # если луч ни с чем не пересекается - возвращает цвет фона
        if closest_shape is None:
            return self.background_color

        # находит точку пересечения луча с объектом, нормаль в этой точке, материал ближайшего объекта
        point = direction.vector_on_scalar_mult(closest_dist) + camera
        # point += camera
        normal: Point = closest_shape.normal(point)
        # material: Material = closest_shape.material

        # вычисляет освещение источников света и итоговый цвет пикселя
        diffuse, specular = self.lighting(point=point, normal=normal, direction=direction,
                                          material=closest_shape.material)

        diffuse_color = (closest_shape.get_color(point)).vector_on_scalar_mult(diffuse)
        specular_color = Point(specular, specular, specular)
        color = diffuse_color + specular_color

        return color

    def run(self) -> list:
        """
        Запуск. Выпускаем лучи в каждый пискель рабочего окна.

        :return: буфер размера width * height, где в каждом элементе храится цвет в системе RGB (3 числа).
        """
        ray_count = self.width * self.height

        for i in range(ray_count):
            p: Point = Point(self.x[i], self.y[i], 1)
            direction: Point = p.normalize()
            color: Point = self.ray(camera=self.camera, direction=direction)

            self.buffer.append(color.to_color())

        # отрисовывает содержимое буфера на картинке
        index = 0
        for x in range(self.width):
            list_y = list()
            for y in range(self.height):
                color = (int(self.buffer[index][0]),
                         int(self.buffer[index][1]),
                         int(self.buffer[index][2]))
                list_y.append(color)
                index += 1
            self.bitmap.append(list_y)

        return self.bitmap
