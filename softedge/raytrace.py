import math
from core import dot, normalize, cross, Sphere, Triangle


class RayTracer(object):
    def intersect(self, ray, obj, backface=True, quick=False):
        return ALGORITHMS[type(obj)](ray, obj, backface=True, quick=False)

    def does_intersect(self, ray, objects):
        """Trace a ray into scene, and stop on any hit
        """
        for obj in objects:
            if self.intersect(ray, obj, backface=True, quick=True):
                return True
        return False

    def cast(self, ray, objects):
        results = []
        for obj in objects:
            result = self.intersect(ray, obj, backface=True, quick=False)
            if result:
                results.append(result)
        if results:
            results.sort(key=lambda i: i.t)
            return results[0]


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


class SphereRayIntersection(RayIntersection):
    def __init__(self, ray, t, sphere):
        self._normal = None
        self.sphere = sphere
        RayIntersection.__init__(self, ray, t, sphere)

    def get_normal(self):
        if self._normal is None:
            self._normal = normalize(self.get_origin() - self.sphere.origin)
        return self._normal


class TriangleRayIntersection(RayIntersection):
    def get_normal(self):
        return normalize(self.renderable.plane.normal)


def intersect_Ray_Sphere(ray, sphere, backface=True, quick=False):
    m = ray.origin - sphere.origin
    c = dot(m, m) - sphere.radius**2.0

    if quick and c <= .0:
        return True

    b = dot(m, ray.direction)
    if b > .0:
        return False

    discr = b * b - c
    if discr < .0:
        return False

    if quick:
        return True

    sqrt_discr = math.sqrt(discr)
    t = -b - sqrt_discr
    if t < .0:
        t = -b + sqrt_discr

    return SphereRayIntersection(ray, t, sphere)


def intersect_Ray_Triangle(ray, triangle, backface=True, quick=False):
    A, B, C = triangle.points
    ab = B - A
    ac = C - A
    n = triangle.plane.normal
    qp = ray.direction * -1

    d = dot(qp, n)
    if (d <= .0 and not backface):
        # Plane and ray are paralell or pointing away
        return False

    ap = ray.origin - A;
    t = dot(ap, n)
    if t < .0:
        return False

    e = cross(qp, ap)
    v = dot(ac, e)
    if (v < .0 or v > d):
        return False

    w = -dot(ab, e)
    if (w <.0 or v + w > d):
        return False

    if quick is not None:
        ood = 1.0 / d
        t *= ood
        return TriangleRayIntersection(ray, t, triangle)

    return True


ALGORITHMS = {
    Sphere: intersect_Ray_Sphere,
    Triangle: intersect_Ray_Triangle
    }
