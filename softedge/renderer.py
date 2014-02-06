import math

from softedge.core import normalize, reflect, Vector3, Ray, hadamard, cross, refract


class Trace(object):
    def __init__(self):
        self.color = Vector3.ZERO
        self.object = None


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

        right = normalize(cross(camera.direction, Vector3.Y))
        up = cross(right, camera.direction)

        for y in xrange(sy, sy + sh):
            for x in xrange(sx, sx + sw):
                xcomp = right * (x * pixel_width - half_width)
                ycomp = up * (y * pixel_height - half_height)
                direction = normalize(camera.direction - xcomp - ycomp)
                ray = Ray(camera.origin, direction)
                trace = Trace()
                self.trace_ray(ray, scene, trace, Vector3(1.0, 1.0, 1.0), scene.refractive_index)
                yield trace.color

    def trace_ray(self, ray, scene, trace, opacity, refractive_index, depth=0):
        # Stop recursion if we have reached full depth, or are fully saturated
        if depth >= self.MAX_DEPTH or all(c >= 1.0 for c in trace.color):
            return

        intersection = self.cast_ray(ray, scene.renderables, backface=False)
        if intersection:
            obj = intersection.renderable
            material = obj.color

            if obj is trace.object:
                # Exiting object
                new_refractive_index = scene.refractive_index
            else:
                # Entering object
                new_refractive_index = material.refractive_index
            trace.object = obj

            # Find lights that are not occluded
            shade = scene.ambient
            for light in scene.lights:
                light_d = normalize(light.origin - intersection.point)
                light_ray = Ray(intersection.point, light_d)
                if not self.test_ray(light_ray, scene.renderables):
                    shade += light.color * material.shade(intersection.normal, light_d, ray.direction)
            trace.color += hadamard(hadamard(shade, material.diffuse_color), opacity)

            # Calculate reflections
            reflect_opacity = hadamard(opacity, material.specular_color)
            if all(i > .1 for i in reflect_opacity):
                reflected_ray = Ray(intersection.point, reflect(ray.direction, intersection.normal))
                self.trace_ray(reflected_ray, scene, trace, reflect_opacity, refractive_index, depth + 1)

            # Calculate refractions
            refract_opacity = hadamard(opacity, material.transparent_color)
            if all(i > .1 for i in refract_opacity):
                refracted_ray = Ray(intersection.point, refract(ray.direction, intersection.normal, refractive_index, new_refractive_index))
                self.trace_ray(refracted_ray, scene, trace, refract_opacity, material.refractive_index, depth + 1)

    def test_ray(self, ray, objects):
        """Trace a ray into scene, and stop on any hit
        """
        for obj in objects:
            if obj.intersect(ray, obj, backface=True, quick=True, epsilon=.1):
                return True
        return False

    def cast_ray(self, ray, objects, backface):
        result = None
        for obj in objects:
            new_result = obj.intersect(ray, obj, backface, quick=False, epsilon=.1)
            if not new_result:
                continue
            elif not result or new_result.t < result.t:
                result = new_result
        return result
