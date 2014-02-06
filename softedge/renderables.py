from softedge.core import dot, cross
from softedge import intersection


class Renderable(object):
    def __init__(self, color):
        self.color = color


class Plane(Renderable):
    def __init__(self, a, b, c):
        self.normal = cross(b-a, c-a)
        self.d = dot(self.normal, a)


class Triangle(Renderable):
    intersect = staticmethod(intersection.intersect_Ray_Triangle)

    def __init__(self, a, b, c, color):
        Renderable.__init__(self, color)
        self.a, self.b, self.c = a, b, c
        self.ab, self.ac = b-a, c-a
        self.plane = Plane(a, b, c)


class Sphere(Renderable):
    intersect = staticmethod(intersection.intersect_Ray_Sphere)

    def __init__(self, origin, radius, color):
        Renderable.__init__(self, color)
        self.origin = origin
        self.radius = radius
