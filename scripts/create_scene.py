from softedge.core import Light, Camera
from softedge.vector import Vector as Point, X, Y, Z
from softedge import color
from softedge.geometry import GeometryGroup, Triangle, Sphere


rbb = Point(500.0,   0.0, 500.0)
lbb = Point(  0.0,   0.0, 500.0)
ltb = Point(  0.0, 500.0, 500.0)
rtb = Point(500.0, 500.0, 500.0)

rbf = Point(500.0, 0.0,   0.0)
lbf = Point(  0.0, 0.0,   0.0)

rtf = Point(500.0, 500.0, 0.0)
ltf = Point(  0.0, 500.0, 0.0)


white = color.Material(color.Color(.0, .0, .0))
red = color.Material(color.Color(.0, -1., -1.))
green = color.Material(color.Color(-1., .0, -1.))

b1 = color.Material(color.Color(.0, .0, .0))
b2 = color.Material(color.Color(.0, .0, .0))

class Scene(object):
    ambient = color.Color(.1, .1, .1)
    lights = [Light(Point(250.0, 499.9, 250.0), color.WHITE)]
    camera = Camera(Point(250.0, 250.0, -800.0), Z)
    geometry = GeometryGroup([
        # Back
        Triangle(lbb, ltb, rtb),
        Triangle(rtb, rbb, lbb),
        # Floor
        Triangle(lbb, rbb, rbf),
        Triangle(rbf, lbf, lbb),
#         # Ceiling
#         Triangle((ltb, ltf, rtf), white),
#         Triangle((rtf, rtb, ltb), white),
        # Left wall
        Triangle(lbb, lbf, ltf),
        Triangle(ltf, ltb, lbb),
        # Right wall
        Triangle(rbb, rtb, rtf),
        Triangle(rtf, rbf, rbb),

        # Balls
        Sphere(Point(150.0,  350.0, 350.0), 100.0),
        Sphere(Point(350.0,  150.0, 150.0), 100.0),
                              ])

import random
for o in Scene.geometry:
    o.radiance = random.choice((X, Y, Z))


def save_scene(filename):
    import cPickle as pickle
    with open(filename, 'w') as f:
        pickle.dump(Scene, f, protocol=0)


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    save_scene(filename)
