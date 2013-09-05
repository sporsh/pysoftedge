import array
import math


class Tuple3(tuple):
    def __new__(cls, x, y, z):
        return tuple.__new__(cls, (x, y, z))

    def __add__(self, other):
        return Tuple3(*(a+b for a, b in zip(self, other)))

    def __sub__(self, other):
        return Tuple3(*(a-b for a, b in zip(self, other)))

    def __mul__(self, scalar):
        return Tuple3(*(c*scalar for c in self))

    def __div__(self, scalar):
        return Tuple3(*(c/scalar for c in self))

    def length(self):
        return math.sqrt(sum(c*c for c in self))

    def resize(self, scalar):
        return self * (scalar / self.length())

    def normalize(self):
        return self.resize(1.0)


def dot(A, B):
    return sum(a * b for a, b in zip(A, B))


Point3 = Tuple3
Vector3 = Tuple3
Color = Tuple3
WHITE = Color(1.0, 1.0, 1.0)
BLACK = Color(.0, .0, .0)
RED = Color(1.0, .0, .0)
GREEN = Color(.0, 1.0, .0)
BLUE = Color(.0, .0, 1.0)
YELLOW = Color(1.0, 1.0, .0)


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def point(self, t):
        return self.origin + (self.direction * t)


class Light(object):
    def __init__(self, origin, intensity=1, color=WHITE):
        self.origin = origin
        self.intensity = intensity
        self.color = color


class Sphere(object):
    def __init__(self, origin, radius, color=RED):
        self.origin = origin
        self.radius = radius
        self.color = color


class Camera(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Scene(object):
    AMBIENT = Color(.1, .1, .1)

    def __init__(self):
        self.renderables = []
        self.lights = []


class Viewport(object):
    MAX_COLOR = 255

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = array.array('B', (0 for n in xrange(width * height * 3)))

    def set_pixel(self, x, y, color):
        i = ((y * self.width) + x) * 3
        self.buffer[i  ] = max(0, min(255, int(color[0] * 255.0)))
        self.buffer[i+1] = max(0, min(255, int(color[1] * 255.0)))
        self.buffer[i+2] = max(0, min(255, int(color[2] * 255.0)))

    def save(self, filename):
        with open('output.ppm', 'wb') as f:
            f.write('P6 %d %d %d\n' % (self.width, self.height, self.MAX_COLOR))
            self.buffer.tofile(f)


def intersect_sphere(sphere, ray, result=True):
    m = ray.origin - sphere.origin
    c = dot(m, m) - sphere.radius**2.0

    if not result and c <= .0:
        return True

    b = dot(m, ray.direction)
    if b > .0:
        return None

    discr = b * b - c
    if discr < .0:
        return None

    if not result:
        return True

    sqrt_discr = math.sqrt(discr)
    t = -b - sqrt_discr
    if t < .0:
        t = -b + sqrt_discr
    return t


def lambert_shade(normal, color, direction):
    i = dot(direction, normal)
    if i < .0:
        return Scene.AMBIENT
    return Scene.AMBIENT + (color * i)

def normal_shade(normal, color, _):
    return (Vector3(1.0, 1.0, 1.0) - normal).normalize()


def raytrace(viewport, scene, camera):
    shader = lambert_shade

    for y in xrange(viewport.height):
        for x in xrange(viewport.width):
            intersections = []
            color = None
            illumination = .0
            ray = Ray(Point3(float(x), float(y), .0), camera.direction)
            for sphere in scene.renderables:
                intersection = intersect_sphere(sphere, ray)
                if intersection is not None:
                    intersections.append((intersection, sphere))
            if intersections:
                intersections.sort(key=lambda i: i[0])
                t, sphere = intersections[0]
                point = ray.point(t)
                color = sphere.color

                for light in scene.lights:
                    occulded = False
                    for s in scene.renderables:
                        if intersect_sphere(s, Ray(ray.point(t-1), (light.origin - point).normalize()), False):
                            occulded = True
                            break
                    if not occulded:
                        normal = (point - sphere.origin).normalize()
                        direction = (light.origin - point).normalize()
                        lambert = max(0, dot(direction, normal) * light.intensity)
                        illumination += lambert
            if color and illumination:
                viewport.set_pixel(x, y, color * illumination)


def main():
    scene = Scene()
    scene.lights.append(Light(Point3(20.0, 120.0, 50.0)))
    scene.lights.append(Light(Point3(700.0, .0, 50.0), .5))
    scene.renderables.append(Sphere(Point3(320.0, 240.0, 400.0), 200.0, YELLOW))
    scene.renderables.append(Sphere(Point3(180.0, 400.0, 320.0), 100.0, GREEN))
    scene.renderables.append(Sphere(Point3(500.0, 400.0, 500.0), 250.0, BLUE))
    camera = Camera(Point3(320.0, 240.0, .0), Vector3(.0, .0, 1.0))

    viewport = Viewport(640, 480)

    raytrace(viewport, scene, camera)

    viewport.save('output.ppm')


if __name__ == '__main__':
    main()
