import math
from core import dot, normalize, cross, Sphere, Triangle


class RayTracer(object):
    def does_intersect(self, ray, objects):
        """Trace a ray into scene, and stop on any hit
        """
        for obj in objects:
            if intersect(ray, obj, backface=True, quick=True):
                return True
        return False

    def cast(self, ray, objects, backface):
        result = None
        for obj in objects:
            new_result = intersect(ray, obj, backface, quick=False)
            if not new_result:
                continue
            elif not result or new_result.t < result.t:
                result = new_result
        return result


class RayIntersection(object):
    def __init__(self, ray, t, renderable):
        self._origin = None
        self.ray = ray
        self.t = t
        self.renderable = renderable

    def get_point(self):
        return self.ray.origin + self.ray.direction * self.t

    def get_normal(self):
        raise NotImplementedError()


class SphereRayIntersection(RayIntersection):
    def __init__(self, ray, t, sphere, inside):
        self._normal = None
        self.sphere = sphere
        self.inside = inside
        RayIntersection.__init__(self, ray, t, sphere)

    def get_normal(self):
        if self._normal is None:
            self._normal = normalize(self.get_point() - self.sphere.origin) * (-1.0 if self.inside else 1.0)
        return self._normal


class TriangleRayIntersection(RayIntersection):
    def get_normal(self):
        return normalize(self.renderable.plane.normal)


def intersect_Ray_Sphere(ray, sphere, backface=True, quick=False):
    inside = False
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
        inside = True
        t = -b + sqrt_discr

    return SphereRayIntersection(ray, t, sphere, inside)


def intersect_Ray_Triangle(ray, triangle, backface=True, quick=False):
    A, B, C = triangle.points
    ab = B - A
    ac = C - A
    n = triangle.plane.normal
    qp = ray.direction * -1

    d = dot(qp, n)
    if (d == .0 or (d < .0 and not backface)):
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


def intersect(ray, obj, backface=True, quick=False):
    return ALGORITHMS[type(obj)](ray, obj, backface=True, quick=False)
