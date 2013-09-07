import math


class Scene(object):
    def __init__(self, background, ambient):
        self.background = background
        self.ambient = ambient
        self.renderables = []
        self.lights = []


class Light(object):
    def __init__(self, origin, intensity):
        self.origin = origin
        self.intensity = intensity

    def get_illumination(self, point):
        """Get illumination details for a specific spatial point
        """
        direction = normalize(self.origin - point)
        return direction, self.intensity


class Camera(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


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
    def __init__(self, points, color):
        Renderable.__init__(self, color)
        self.points = points
        self.plane = Plane(points)


class Sphere(Renderable):
    def __init__(self, origin, radius, color):
        Renderable.__init__(self, color)
        self.origin = origin
        self.radius = radius


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def point(self, t):
        return self.origin + (self.direction * t)


class Tuple3(tuple):
    def __new__(cls, x, y, z):
        return tuple.__new__(cls, (x, y, z))

    def __add__(self, other):
        return type(self)(*(a+b for a, b in zip(self, other)))

    def __sub__(self, other):
        return type(self)(*(a-b for a, b in zip(self, other)))

    def __mul__(self, scalar):
        return type(self)(*(c*scalar for c in self))

    def __div__(self, scalar):
        return type(self)(*(c/scalar for c in self))

    def length(self):
        return math.sqrt(sum(c*c for c in self))

Point3 = Tuple3
Vector3 = Tuple3


def dot(A, B):
    """Compute the dot product of two vectors
    """
    return sum(a * b for a, b in zip(A, B))


def cross(A, B):
    """Compute the cross product of two vectors
    """
    return Tuple3(A[1]*B[2] - A[2]*B[1],
                  A[2]*B[0] - A[0]*B[2],
                  A[0]*B[1] - A[1]*B[0],)


def resize(vector, scalar):
    return vector * (scalar / vector.length())


def normalize(vector):
    """Normalize a vector
    """
    return resize(vector, 1.0)

def reflect(vector, normal):
    return vector - (normal * (2 * dot(vector, normal)))
