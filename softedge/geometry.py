from softedge.intersection import intersect_Ray_Sphere, intersect_Ray_Triangle


class Plane(object):
    def __init__(self, a, b, c):
        self.normal = (b-a).cross(c-a)
        self.d = self.normal.dot(a)


class Triangle(object):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
        self.ab, self.ac = b-a, c-a
        self.plane = Plane(a, b, c)

    def intersect(self, ray, backface, epsilon):
        return intersect_Ray_Triangle(ray, self, backface, False, epsilon)

    def test(self, ray, backface, epsilon):
        return intersect_Ray_Triangle(ray, self, backface, True, epsilon)


class Sphere(object):
    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius

    def intersect(self, ray, backface, epsilon):
        return intersect_Ray_Sphere(ray, self, backface, False, epsilon)

    def test(self, ray, backface, epsilon):
        return intersect_Ray_Sphere(ray, self, backface, True, epsilon)


class GeometryGroup(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def intersect(self, ray, backface, epsilon):
        result = None
        for obj in self:
            new_result = obj.intersect(ray, backface, epsilon)
            if not new_result:
                continue
            elif not result or new_result.t < result.t:
                result = new_result
        return result

    def test(self, ray, backface, epsilon):
        for obj in self:
            if obj.test(ray, backface, epsilon):
                return True
        return False
