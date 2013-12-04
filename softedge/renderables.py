from softedge.core import dot, cross
from softedge import intersection

class Renderable(object):
    def __init__(self, color):
        self.color = color

    def accept(self, visitor, args, kwargs):
        return visitor.visit(self, args, kwargs)


class Plane(Renderable):
    def __init__(self, points):
        a, b, c = points
        self.normal = cross(b-a, c-a)
        self.d = dot(self.normal, a)


class Triangle(Renderable):
    intersect = staticmethod(intersection.intersect_Ray_Triangle)

    def __init__(self, points, color):
        Renderable.__init__(self, color)
        self.points = points
        self.plane = Plane(points)


class Sphere(Renderable):
    intersect = staticmethod(intersection.intersect_Ray_Sphere)

    def __init__(self, origin, radius, color):
        Renderable.__init__(self, color)
        self.origin = origin
        self.radius = radius
