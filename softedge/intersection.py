import math
from softedge.core import dot, normalize, cross


class RayIntersection(object):
    def __init__(self, ray, t, renderable):
        self.point = ray.origin + ray.direction * t
        self.ray = ray
        self.t = t
        self.renderable = renderable


class SphereRayIntersection(RayIntersection):
    def __init__(self, ray, t, sphere, inside):
        RayIntersection.__init__(self, ray, t, sphere)
        self.normal = normalize(self.point - sphere.origin)
        if inside:
            self.normal = self.normal * -1
        self.sphere = sphere
        self.inside = inside


class TriangleRayIntersection(RayIntersection):
    def __init__(self, ray, t, renderable):
        RayIntersection.__init__(self, ray, t, renderable)
        self.normal = normalize(renderable.plane.normal)


def intersect_Ray_Sphere(ray, sphere, backface, quick, epsilon):
    m = ray.origin - sphere.origin
    c = dot(m, m) - sphere.radius*sphere.radius

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
    qp = ray.direction * -1

    d = dot(qp, triangle.plane.normal)
    if (d == .0 or (d < .0 and not backface)):
        # Plane and ray are paralell or pointing away
        return False

    ap = ray.origin - triangle.a
    t = dot(ap, triangle.plane.normal)
    if t < .0:
        return False

    e = cross(qp, ap)
    v = dot(triangle.ac, e)
    if (v < .0 or v > d):
        return False

    w = -dot(triangle.ab, e)
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
