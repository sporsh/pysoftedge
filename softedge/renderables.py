from softedge import geometry


class Renderable(object):
    def __init__(self, material):
        self.material = material


class Sphere(Renderable, geometry.Sphere):
    def __init__(self, material, origin, radius):
        Renderable.__init__(self, material)
        geometry.Sphere.__init__(self, origin, radius)


class Triangle(geometry.Triangle, Renderable):
    def __init__(self, material, a, b, c):
        Renderable.__init__(self, material)
        geometry.Triangle.__init__(self, a, b, c)
