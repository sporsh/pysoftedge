import math


class Vector(tuple):
    def __new__(cls, x, y, z):
        return tuple.__new__(cls, (x, y, z))

    def __add__(self, other):
        return type(self)(self[0] + other[0],
                          self[1] + other[1],
                          self[2] + other[2])

    def __sub__(self, other):
        return type(self)(self[0] - other[0],
                          self[1] - other[1],
                          self[2] - other[2])

    def __mul__(self, scalar):
        return type(self)(self[0] * scalar,
                          self[1] * scalar,
                          self[2] * scalar)

    def __div__(self, scalar):
        return type(self)(self[0] / scalar,
                          self[1] / scalar,
                          self[2] / scalar)

    def dot(self, other):
        return self[0] * other[0] + self[1] * other[1] + self[2] * other[2]

    def cross(self, other):
        return type(self)(self[1] * other[2] - self[2] * other[1],
                          self[2] * other[0] - self[0] * other[2],
                          self[0] * other[1] - self[1] * other[0])

    def length(self):
        return math.sqrt(self.dot(self))

    def resize(self, scalar):
        return self * (scalar / self.length())

    def normalize(self):
        return self.resize(1.0)

    def reflect(self, normal):
        return self - (normal * (2 * self.dot(normal)))

    def refract(self, normal, n1, n2):
        n = n1 / n2
        cosi = -normal.dot(self)
        cost2 = 1.0 - n * n * (1.0 - cosi * cosi)
        return (self * n) + (normal * (n * cosi - math.sqrt(abs(cost2))))


ZERO = Vector(.0, .0, .0)
X = Vector(1.0, .0, .0)
Y = Vector(.0, 1.0, .0)
Z = Vector(.0, .0, 1.0)
