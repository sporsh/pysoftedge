from softedge.vector import Vector as Color
import math
import struct


WHITE = Color(1.0, 1.0, 1.0)
BLACK = Color(.0, .0, .0)
RED = Color(1.0, .0, .0)
GREEN = Color(.0, 1.0, .0)
BLUE = Color(.0, .0, 1.0)
YELLOW = Color(1.0, 1.0, .0)

GRAY = Color(.5, .5, .5)
LIGHT_GRAY = Color(.75, .75, .75)
DARK_GRAY = Color(.25, .25, .25)


def to_intv(color):
    for component in color:
        yield min(int(component * 255.), 255)
    yield 0xff

def to_str(color):
    return struct.pack('4B', *rgba(color))


class Material(object):
    def __init__(self, radiance):
        self.radiance = radiance


class _Material(object):
    def __init__(self, diffuse_color=GRAY, specular_color=BLACK, transparent_color=BLACK):

        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.transparent_color = transparent_color
        self.diffuse_intensity = 1.0
        self.specular_intensity = .0
        self.specular_hardness = 50
        self.refractive_index = 1.6

    def shade(self, normal, light_direction, view_direction):
        diffuse = specular = .0
        if self.diffuse_intensity > .0:
            diffuse = max(.0, normal.dot(light_direction)) * self.diffuse_intensity
        H = (light_direction + view_direction).normalize()
        if self.specular_intensity > .0:
            specular = math.pow(max(.0, normal.dot(H)), self.specular_hardness)
            specular *= self.specular_intensity
        return diffuse + specular

def rgba(color):
    r = int(min(max(0, color[0]), 1) * 0xff)
    g = int(min(max(0, color[1]), 1) * 0xff)
    b = int(min(max(0, color[2]), 1) * 0xff)
    a = 0xff
    return r, g, b, a
