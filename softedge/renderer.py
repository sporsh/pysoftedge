from softedge.canvas import Canvas
from softedge.raytrace import RayTracer
from softedge.core import dot, normalize, Point3, Vector3, Ray


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
                ray = Ray(Point3(float(x), float(y), .0), camera.direction)
                intersection = self.raytracer.cast(ray, scene.renderables)
                if intersection:
                    point = intersection.get_origin()

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
                        shade += self.shader(intersection.get_normal(), direction) * intensity
                    color = intersection.renderable.color * shade

                    self.canvas.set_pixel(x, y, color)

        filename = 'rtr_scene_camera'
        self.canvas.save(filename)


def shade_lambert(normal, direction):
    return max(.0, dot(direction, normal))

def shade_flat(normal, direction):
    return 1.0

def shade_normal(normal, direction):
    return normalize(Vector3(1.0, 1.0, 1.0) - normal)
