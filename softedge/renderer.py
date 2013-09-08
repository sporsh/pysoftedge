from softedge.framebuffer import Framebuffer
from softedge.raytrace import RayTracer
from softedge.core import dot, normalize, reflect, Vector3, Ray
import math


class RaytraceRenderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = Framebuffer(width, height)

        self.raytracer = RayTracer()
        self.shader = shade_lambert

    def render(self, scene, camera):
        fov = 45
        fov_radians = math.pi * fov / 2.0 / 180.0
        half_width = math.tan(fov_radians)
        half_height = .75 * half_width
        pixel_width = half_width * 2 / self.framebuffer.width
        pixel_height = half_height * 2 / self.framebuffer.height

        for y in xrange(self.height):
            for x in xrange(self.width):
                results = []
                xcomp = Vector3.X * (x * pixel_width - half_width)
                ycomp = Vector3.Y * (y * pixel_height - half_height)
                direction = normalize(camera.direction + xcomp + ycomp)
                ray = Ray(camera.origin, direction)
                self.trace(ray, scene, results, 2)
                color = reduce(lambda a,b: a+b, results) / len(results)
                self.framebuffer.set_pixel(x, y, color)

        filename = 'rtr_scene_camera'
        self.framebuffer.save(filename)

    def trace(self, ray, scene, results, depth):
        intersection = self.raytracer.cast(ray, scene.renderables, backface=False)
        if intersection:
            point = intersection.get_origin()
            normal = intersection.get_normal()

            # Find lights that are not occluded
            lights = []
            for light in scene.lights:
                direction = normalize(light.origin - point)
                ray = Ray(point, direction)
                if not self.raytracer.does_intersect(ray, scene.renderables):
                    lights.append(light)

            shade = scene.ambient
            for light in lights:
                direction, intensity = light.get_illumination(point)
                shade += self.shader(normal, direction) * intensity
            results.append(intersection.renderable.color * shade)
            if len(results) <= depth:
                reflected_ray = Ray(point, reflect(ray.direction, normal))
                self.trace(reflected_ray, scene, results, depth)
        else:
            results.append(scene.background)

def shade_lambert(normal, direction):
    return max(.0, dot(direction, normal))

def shade_flat(normal, direction):
    return 1.0

def shade_normal(normal, direction):
    return normalize(Vector3(1.0, 1.0, 1.0) - normal)
