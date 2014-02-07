import math

from softedge import vector
from softedge.vector import Vector, ZERO
from softedge.core import Ray
import random
random.seed()

EPSILON = .1
MAX_DEPTH = 5

class Trace(object):
    def __init__(self, ray, radiance):
        self.ray = ray
        self.radiance = [radiance]
        self.depth = 0


class Sampler(object):
    def __init__(self, geometry, lights):
        self.geometry = geometry
        self.lights = lights
        self.ambient = Vector(.2, .2, .2)

    def sample(self, camera, width, height, sx, sy, sw, sh):
        fov = 45. / 2
        fov_radians = fov * math.pi / 180.
        half_width = math.tan(fov_radians)
        aspect = float(height) / width
        half_height = aspect * half_width
        pixel_width = half_width * 2 / width
        pixel_height = half_height * 2 / height

        right = (camera.direction.cross(vector.Y)).normalize()
        up = right.cross(camera.direction)

        for y in xrange(sy, sy + sh):
            for x in xrange(sx, sx + sw):
                radiance, samples = ZERO, 0
                for _ in xrange(10):
                    xcomp = right * ((x + random.random() - .5) * pixel_width - half_width)
                    ycomp = up * ((y + random.random() - .5) * pixel_height - half_height)
                    direction = (camera.direction - xcomp - ycomp).normalize()
                    ray = Ray(camera.origin, direction)
                    for sample in self.trace(ray):
                        radiance += sample
                        samples += 1
                yield radiance / samples

    def trace(self, ray):
        i = self.geometry.intersect(ray, False, EPSILON)
        if i:
            for radiance in random.choice((self.radiance, self.reflect))(ray, i):
                yield radiance
        else:
            yield ZERO

    def reflect(self, ray, i):
        ray.origin = i.point
        ray.direction = ray.direction.reflect(i.normal)
        for radiance in self.trace(ray):
            yield radiance

    def radiance(self, ray, i):
        """Sample outgoint radiance to ray from surface at intersection i
        """
        yield Vector(-.5, -.5, -.5) * max(0, i.normal.dot(ray.direction * -1))
#         yield i.renderable.radiance * max(0, i.normal.dot(ray.direction * -1))
        for irradiance in self.irradiance(i):
            yield irradiance

    def irradiance(self, i):
        """Sample incoming (direct) irradiance at a given intersection point
        """
        for light in self.lights:
            ray = Ray(i.point, (light.origin - i.point).normalize())
            if not self.geometry.test(ray, True, EPSILON):
                # Light is not occluded
                yield light.radiance * max(0, i.normal.dot(ray.direction))


class RaytraceRenderer(object):
    MAX_DEPTH = 5

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render_region(self, scene, camera, sx, sy, sw, sh):
        fov = 45. / 2
        fov_radians = fov * math.pi / 180.
        half_width = math.tan(fov_radians)
        aspect = float(self.height) / self.width
        half_height = aspect * half_width
        pixel_width = half_width * 2 / self.width
        pixel_height = half_height * 2 / self.height

        right = (camera.direction.cross(vector.Y)).normalize()
        up = right.cross(camera.direction)

        for y in xrange(sy, sy + sh):
            for x in xrange(sx, sx + sw):
                xcomp = right * (x * pixel_width - half_width)
                ycomp = up * (y * pixel_height - half_height)
                direction = (camera.direction - xcomp - ycomp).normalize()
                ray = Ray(camera.origin, direction)
                trace = Trace()
                self.trace_ray(ray, scene, trace, Vector(1.0, 1.0, 1.0), scene.refractive_index)
                yield trace.color

    def trace_ray(self, ray, scene, trace, opacity, refractive_index, depth=0):
        # Stop recursion if we have reached full depth, or are fully saturated
        if depth >= self.MAX_DEPTH or all(c >= 1.0 for c in trace.color):
            return

        intersection = self.cast_ray(ray, scene.renderables, backface=False)
        if intersection:
            obj = intersection.renderable
            material = obj.material

#             if obj is trace.object:
#                 # Exiting object
#                 new_refractive_index = scene.refractive_index
#             else:
#                 # Entering object
#                 new_refractive_index = material.refractive_index
#             trace.object = obj

#             for _ in xrange(subsamples):
#                 random.select(absorb, reflect, transmit)

            # -- ABSORB
            # Find lights that are not occluded
            irradiance = scene.ambient
            for light in scene.lights:
                light_d = (light.origin - intersection.point).normalize()
                light_ray = Ray(intersection.point, light_d)
                if not self.test_ray(light_ray, scene.renderables):
                    irradiance += light.radiance * max(0, intersection.normal.dot(light_ray.direction))
            radiance = material.radiance * max(0, intersection.normal.dot(ray.direction*-1))
            trace.color += radiance + irradiance
            return

            # -- REFLECT
            # Calculate reflections
            reflect_opacity = hadamard(opacity, material.specular_color)
            if all(i > .1 for i in reflect_opacity):
                reflected_ray = Ray(intersection.point, ray.direction.reflect(intersection.normal))
                self.trace_ray(reflected_ray, scene, trace, reflect_opacity, refractive_index, depth + 1)

            # -- TRANSMIT
            # Calculate refractions
            refract_opacity = hadamard(opacity, material.transparent_color)
            if all(i > .1 for i in refract_opacity):
                refracted_ray = Ray(intersection.point, ray.direction.refract(intersection.normal, refractive_index, new_refractive_index))
                self.trace_ray(refracted_ray, scene, trace, refract_opacity, material.refractive_index, depth + 1)

    def transmit(self):
        pass

    def reflect(self):
        pass

    def absorb(self):
        """record all the absorbants on the recrsion way, apply here (direct light)
        """
        pass
