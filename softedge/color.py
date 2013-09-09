from core import Tuple3 as Color
from softedge.core import dot, normalize
import math


WHITE = Color(1.0, 1.0, 1.0)
BLACK = Color(.0, .0, .0)
RED = Color(1.0, .0, .0)
GREEN = Color(.0, 1.0, .0)
BLUE = Color(.0, .0, 1.0)
YELLOW = Color(1.0, 1.0, .0)

GRAY = Color(.5, .5, .5)
LIGHT_GRAY = Color(.75, .75, .75)
DARK_GRAY = Color(.25, .25, .25)


class Material(object):
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
            diffuse = max(.0, dot(normal, light_direction)) * self.diffuse_intensity
        H = normalize(light_direction + view_direction)
        if self.specular_intensity > .0:
            specular = math.pow(max(.0, dot(normal, H)), self.specular_hardness)
            specular *= self.specular_intensity
        return diffuse + specular
