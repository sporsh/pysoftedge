from softedge.geometry import Sphere, Triangle


class Renderable(object):
    def __init__(self, material):
        self.material = material


class Sphere(Renderable, Sphere):
    def __init__(self, material, origin, radius):
        Renderable.__init__(self, material)
        Sphere.__init__(self, origin, radius)


class Triangle(Triangle, Renderable):
    def __init__(self, material, a, b, c):
        Renderable.__init__(self, material)
        Triangle.__init__(self, a, b, c)
