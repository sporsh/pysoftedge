import math


class Scene(object):
    def __init__(self, background, ambient):
        self.background = background
        self.ambient = ambient
        self.renderables = []
        self.lights = []
        self.refractive_index = 1.0


class Light(object):
    def __init__(self, origin, color, intensity=1.0):
        self.origin = origin
        self.color = color * intensity

    def get_illumination(self, point):
        """Get illumination details for a specific spatial point
        """
        direction = normalize(self.origin - point)
        return direction, self.intensity


class Camera(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Tuple3(tuple):
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

    def length(self):
        return math.sqrt(dot(self, self))


Point3 = Tuple3
Vector3 = Tuple3
Vector3.ZERO = Vector3(.0, .0, .0)
Vector3.X = Vector3(1.0, .0, .0)
Vector3.Y = Vector3(.0, 1.0, .0)
Vector3.Z = Vector3(.0, .0, 1.0)


def dot(A, B):
    return A[0] * B[0] + A[1] * B[1] + A[2] * B[2]


def cross(A, B):
    return type(A)(A[1] * B[2] - A[2] * B[1],
                   A[2] * B[0] - A[0] * B[2],
                   A[0] * B[1] - A[1] * B[0])


def hadamard(A, B):
    return type(A)(A[0] * B[0], A[1] * B[1], A[2] * B[2])


def resize(vector, scalar):
    return vector * (scalar / vector.length())


def normalize(vector):
    return resize(vector, 1.0)


def reflect(vector, normal):
    return vector - (normal * (2 * dot(vector, normal)))


def refract(vector, normal, n1, n2):
    n = n1 / n2
    cosi = -dot(normal, vector)
    cost2 = 1.0 - n * n * (1.0 - cosi * cosi)
    return (vector * n) + (normal * (n * cosi - math.sqrt(abs(cost2))))
