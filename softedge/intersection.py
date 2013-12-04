import math
from softedge.core import dot, normalize, cross


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


def intersect_Ray_Sphere(ray, sphere, backface, quick, epsilon):
    m = ray.origin - sphere.origin
    c = dot(m, m) - sphere.radius**2.0

    if quick and c < -epsilon:
        return True

    b = dot(m, ray.direction)
    if b > .0:
        return False

    discr = b * b - c
    if discr < .0:
        return False

    if quick:
        return True

    inside = False
    sqrt_discr = math.sqrt(discr)
    t = -b - sqrt_discr
    if t < epsilon:
        inside = True
        t = -b + sqrt_discr

    if t < epsilon:
        return False

    return SphereRayIntersection(ray, t, sphere, inside)


def intersect_Ray_Triangle(ray, triangle, backface, quick, epsilon):
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

    if quick:
        return True

    ood = 1.0 / d
    t *= ood

    return TriangleRayIntersection(ray, t, triangle)


def quadric(a, b, c):
    disc = b * b - 4 * a * c
    if disc < 0:
        return

    disc = math.sqrt(disc)
    if b < 0:
        q = -0.5 * (b - disc)
    else:
        q = -0.5 * (b + disc)

    t0, t1 = q / a, c / q
    return (t0, t1) if t0 < t1 else (t1, t0)


def intersect_Ray_Sphere_quadric(ray, sphere, backface, quick, epsilon):
    oc = ray.origin - sphere.origin

    qa = dot(ray.direction, ray.direction)
    qb = dot(ray.direction, oc) * 2
    qc = dot(oc, oc) - sphere.radius**2.
    t = quadric(qa, qb, qc)
    if t:
        t0, t1 = t
        if t1 <= epsilon:
            return False
        elif t0 > epsilon:
            return SphereRayIntersection(ray, t0, sphere, False)
        else:
            return SphereRayIntersection(ray, t1, sphere, True)
