from softedge.core import Light, Camera
from softedge.vector import Vector as Point, X, Y, Z
from softedge import color
from softedge.geometry import GeometryGroup
from softedge.renderables import Triangle, Sphere

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

mirror = color.Material(color.Color(.0, .0, .0))
glass = color.Material(color.Color(.0, .0, .0))

class Scene(object):
    ambient = color.Color(.1, .1, .1)
    lights = [Light(Point(250.0, 499.9, 250.0), color.WHITE),
#               Light(Point(20.0, 20.0, 20.0), color.WHITE),
              ]
    camera = Camera(Point(250.0, 250.0, -800.0), Z)
    geometry = GeometryGroup([
        # Back
        Triangle(white, lbb, ltb, rtb),
        Triangle(white, rtb, rbb, lbb),
        # Floor
        Triangle(white, lbb, rbb, rbf),
        Triangle(white, rbf, lbf, lbb),
#         # Ceiling
#         Triangle((ltb, ltf, rtf), white),
#         Triangle((rtf, rtb, ltb), white),
        # Left wall
        Triangle(red, lbb, lbf, ltf),
        Triangle(red, ltf, ltb, lbb),
        # Right wall
        Triangle(green, rbb, rtb, rtf),
        Triangle(green, rtf, rbf, rbb),

        # Balls
        Sphere(mirror, Point(150.0,  350.0, 350.0), 100.0),
        Sphere(glass, Point(350.0,  150.0, 150.0), 100.0),
                              ])

def save_scene(filename):
    import cPickle as pickle
    with open(filename, 'w') as f:
        pickle.dump(Scene, f, protocol=0)


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    save_scene(filename)
