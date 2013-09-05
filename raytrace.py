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
    def __init__(self, origin, intensity):
        self.origin = origin
        self.intensity = intensity

    def is_occluded(self, origin, occluders):
        for occluder in occluders:
            direction = (self.origin - origin).normalize()
            ray = Ray(origin, direction)
            if occluder.intersect(ray, result=False):
                return True
        return False

    def get_illumination(self, origin):
        """Get illumination details for a specific spatial point
        """
        direction = (self.origin - origin).normalize()
        return direction, self.intensity


class Renderable(object):
    def __init__(self, origin, color):
        self.origin = origin
        self.color = color

    def intersect(self, ray, result=True, backface=True):
        raise NotImplementedError()


class Sphere(Renderable):
    def __init__(self, origin, radius, color):
        Renderable.__init__(self, origin, color)
        self.radius = radius

    def intersect(self, ray, result=True, backface=True):
        m = ray.origin - self.origin
        c = dot(m, m) - self.radius**2.0

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
        return SphereRayIntersection(ray, t, self)


class Surface(object):
    def __init__(self, origin, normal, color):
        self.origin = origin
        self.normal = normal
        self.color = color

    def illuminate(self, scene, mode='lambert'):
        if mode == 'lambert':
            lights = (l for l in scene.lights if not l.is_occluded(self.origin, scene.renderables))
            return self.color * (scene.ambient + self.shade_lambert(lights))
        elif mode == 'flat':
            return self.color

    def shade_lambert(self, lights):
        illumination = .0
        for light in lights:
            direction, intensity = light.get_illumination(self.origin)
            illumination += max(0, dot(direction, self.normal) * intensity)
        return illumination


class RayIntersection(object):
    def __init__(self, ray, t, renderable):
        self._origin = None
        self.ray = ray
        self.t = t
        self.renderable = renderable

    def get_origin(self, offset=.1):
        if self._origin is None:
            self._origin = self.ray.point(self.t - offset)
        return self._origin

    def get_normal(self):
        raise NotImplementedError()

    def get_surface(self):
        return Surface(self.get_origin(),
                       self.get_normal(),
                       self.renderable.color)


class SphereRayIntersection(RayIntersection):
    def __init__(self, ray, t, sphere):
        self._normal = None
        self.sphere = sphere
        RayIntersection.__init__(self, ray, t, sphere)

    def get_normal(self):
        if self._normal is None:
            self._normal = (self.get_origin() - self.sphere.origin).normalize()
        return self._normal


class Camera(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Scene(object):
    def __init__(self):
        self.ambient = .05
        self.renderables = []
        self.lights = []


class Canvas(object):
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
        filename += '.ppm' if not 'filename.'.endswith('.ppm') else ''
        with open(filename, 'wb') as f:
            f.write('P6 %d %d 255\n' % (self.width, self.height))
            self.buffer.tofile(f)


class RaytraceRenderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = Canvas(width, height)

    def render(self, scene, camera):
        tracer = RayTracer()
        for y in xrange(self.height):
            for x in xrange(self.width):
                ray = Ray(Point3(float(x), float(y), .0), camera.direction)
                color = tracer.trace(ray, scene)
                if color:
                    self.canvas.set_pixel(x, y, color)

        filename = 'rtr_scene_camera'
        self.canvas.save(filename)


class RayTracer(object):
    def trace(self, ray, scene):
        trace = []
        for renderable in scene.renderables:
            intersection = renderable.intersect(ray)
            if intersection is not None:
                trace.append(intersection)
        if trace:
            trace.sort(key=lambda i: i.t)
            surface = trace.pop(0).get_surface()
            return surface.illuminate(scene)


def main():
    scene = Scene()
    scene.lights.append(Light(Point3(20.0, 120.0, 100.0), .8))
    scene.lights.append(Light(Point3(700.0, .0, .0), .4))
    scene.renderables.append(Sphere(Point3(320.0, 240.0, 400.0), 200.0, YELLOW))
    scene.renderables.append(Sphere(Point3(450.0, 200.0, 220.0), 40.0, RED))
    scene.renderables.append(Sphere(Point3(230.0, 350.0, 320.0), 100.0, GREEN))
    scene.renderables.append(Sphere(Point3(500.0, 400.0, 500.0), 250.0, BLUE))

    camera = Camera(Point3(320.0, 240.0, .0), Vector3(.0, .0, 1.0))

    renderer = RaytraceRenderer(640, 480)
    renderer.render(scene, camera)


if __name__ == '__main__':
    main()
