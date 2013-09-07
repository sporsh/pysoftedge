from softedge.canvas import Canvas
from softedge.raytrace import RayTracer
from softedge.core import dot, normalize, reflect, Point3, Vector3, Ray


class RaytraceRenderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = Canvas(width, height)

        self.raytracer = RayTracer()
        self.shader = shade_lambert

    def render(self, scene, camera):
        for y in xrange(self.height):
            for x in xrange(self.width):
                results = []
                ray = Ray(Point3(float(x), float(y), .0), camera.direction)
                self.trace(ray, scene, results, 1)
                color = reduce(lambda a,b: a+b, results) / len(results)
                self.canvas.set_pixel(x, y, color)

        filename = 'rtr_scene_camera'
        self.canvas.save(filename)

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
