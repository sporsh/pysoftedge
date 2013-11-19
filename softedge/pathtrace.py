from softedge.framebuffer import Framebuffer
from softedge.raytrace import RayTracer
from softedge.core import normalize, reflect, Vector3, Ray, hadamard, cross, refract
import math


class PathTraceRenderer(object):
    MAX_DEPTH = 10

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = Framebuffer(width, height)
        self.deepest_trace = 0

        self.raytracer = RayTracer()

    def render(self, scene, camera):
        fov = 45
        fov_radians = math.pi * fov / 2.0 / 180.0
        half_width = math.tan(fov_radians)
        half_height = .75 * half_width
        pixel_width = half_width * 2 / self.framebuffer.width
        pixel_height = half_height * 2 / self.framebuffer.height

        right = normalize(cross(camera.direction, Vector3.Y))
        up = cross(right, camera.direction)

        for y in xrange(self.height):
            for x in xrange(self.width):
                xcomp = right * (x * pixel_width - half_width)
                ycomp = up * (y * pixel_height - half_height)
                direction = normalize(camera.direction - xcomp - ycomp)
                ray = Ray(camera.origin, direction)
                trace = {'color': Vector3.ZERO}
                self.trace(ray, scene, trace, Vector3(1.0, 1.0, 1.0), scene.refractive_index, None)
                self.framebuffer.set_pixel(x, y, trace['color'])

        filename = 'rtr_scene_camera'
        self.framebuffer.save(filename)

    def trace(self, ray, scene, trace, opacity, refractive_index, prev, depth=0):
        if depth > self.deepest_trace:
            self.deepest_trace = depth
            print "Depth:", depth

        intersection = self.raytracer.cast(ray, scene.renderables, backface=False)
        if intersection:
            obj = intersection.renderable
            material = obj.color
            normal = intersection.get_normal()
            view_d = normalize(ray.direction * -1)

            if obj is prev:
                # Exiting object
                new_refractive_index = scene.refractive_index
                offset = normal * .1 # Slightliy outside the object
            else:
                # Entering object
                new_refractive_index = material.refractive_index
                offset = normal * -.1 # Slightliy inside the object
            point = intersection.get_point()

            # Find lights that are not occluded
            shade = scene.ambient
            for light in scene.lights:
                light_ray = Ray(point, normalize(light.origin - point))
                if not self.raytracer.does_intersect(light_ray, scene.renderables):
                    light_d = normalize(light.origin - point)
                    shade += light.color * material.shade(normal, light_d, view_d)
            trace['color'] += hadamard(hadamard(shade, material.diffuse_color), opacity)

            # Stop recursion if we are fully saturated
            if all(c >= 1.0 for c in trace['color']):
                return

            # Calculate refractions
            refract_opacity = hadamard(opacity, material.transparent_color)
            if depth < self.MAX_DEPTH and all(i > .1 for i in refract_opacity):
                refracted_ray = Ray(point + offset, refract(ray.direction, normal, refractive_index, new_refractive_index))
                self.trace(refracted_ray, scene, trace, refract_opacity, material.refractive_index, obj, depth + 1)

            # Calculate reflections
            reflect_opacity = hadamard(opacity, material.specular_color)
            if depth < self.MAX_DEPTH and all(i > .1 for i in reflect_opacity):
                reflected_ray = Ray(point, reflect(ray.direction, normal))
                self.trace(reflected_ray, scene, trace, reflect_opacity, refractive_index, obj, depth + 1)

    def transmit(self):
        pass

    def reflect(self):
        pass

    def absorb(self):
        pass

