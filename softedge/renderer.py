from softedge.raytrace import RayTracer
from softedge.core import normalize, reflect, Vector3, Ray, hadamard, cross, refract
import math
from softedge import color


class Trace(object):
    def __init__(self):
        self.color = Vector3.ZERO


class RaytraceRenderer(object):
    MAX_DEPTH = 5

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.raytracer = RayTracer()

    def render(self, scene, camera):
        filename = 'rtr_scene_camera.pam'
        with open(filename, 'wb') as f:
            f.write('P7\n'
                    'WIDTH %d\n'
                    'HEIGHT %d\n'
                    'DEPTH 4\n'
                    'MAXVAL 255\n'
                    'TUPLTYPE RGB_ALPHA\n'
                    'ENDHDR\n' % (self.width, self.height))
            for color_ in self.render_region(scene, camera, 0, 0, self.width, self.height):
                f.write(color.to_str(color_))
        print "Number of rays:", Ray.NUM, "tuples:", Vector3.NUM

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
                self.trace(ray, scene, trace, Vector3(1.0, 1.0, 1.0), scene.refractive_index, None)
                yield trace.color

    def trace(self, ray, scene, trace, opacity, refractive_index, prev, depth=0):
        intersection = self.raytracer.cast(ray, scene.renderables, backface=False)
        if intersection:
            obj = intersection.renderable
            material = obj.color
            normal = intersection.get_normal()
            view_d = normalize(ray.direction * -1)

            if obj is prev:
                # Exiting object
                new_refractive_index = scene.refractive_index
            else:
                # Entering object
                new_refractive_index = material.refractive_index
            point = intersection.get_point()

            # Find lights that are not occluded
            shade = scene.ambient
            for light in scene.lights:
                light_ray = Ray(point, normalize(light.origin - point))
                if not self.raytracer.does_intersect(light_ray, scene.renderables):
                    light_d = normalize(light.origin - point)
                    shade += light.color * material.shade(normal, light_d, view_d)
            trace.color += hadamard(hadamard(shade, material.diffuse_color), opacity)

            # Stop recursion if we have reached full depth, or are fully saturated
            if depth >= self.MAX_DEPTH or all(c >= 1.0 for c in trace.color):
                return

            # Calculate reflections
            reflect_opacity = hadamard(opacity, material.specular_color)
            if all(i > .1 for i in reflect_opacity):
                reflected_ray = Ray(point, reflect(ray.direction, normal))
                self.trace(reflected_ray, scene, trace, reflect_opacity, refractive_index, obj, depth + 1)

            # Calculate refractions
            refract_opacity = hadamard(opacity, material.transparent_color)
            if all(i > .1 for i in refract_opacity):
                refracted_ray = Ray(point, refract(ray.direction, normal, refractive_index, new_refractive_index))
                self.trace(refracted_ray, scene, trace, refract_opacity, material.refractive_index, obj, depth + 1)
