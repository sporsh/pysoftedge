from softedge.core import Scene, Light, Point3
from softedge.renderables import Sphere, Triangle
from softedge import color


scene = Scene(color.BLACK, ambient=color.Color(.1, .1, .1))

scene.lights.append(Light(Point3(250.0, 499.9, 250.0), color.WHITE))

rbb = Point3(500.0,   0.0, 500.0)
lbb = Point3(  0.0,   0.0, 500.0)
ltb = Point3(  0.0, 500.0, 500.0)
rtb = Point3(500.0, 500.0, 500.0)

rbf = Point3(500.0, 0.0,   0.0)
lbf = Point3(  0.0, 0.0,   0.0)

rtf = Point3(500.0, 500.0, 0.0)
ltf = Point3(  0.0, 500.0, 0.0)

white = color.Material(color.Color(.8, .8, .8))
white.specular_intensity = 1.0
red = color.Material(color.Color(.8, .4, .4), color.Color(.8, .4, .4))
red.specular_intensity = 1.0
green = color.Material(color.Color(.4, .8, .4), color.Color(.4, .8, .4))
green.specular_intensity = 1.0

# Back
scene.renderables.append(Triangle(lbb, ltb, rtb, white))
scene.renderables.append(Triangle(rtb, rbb, lbb, white))

# Floor
scene.renderables.append(Triangle(lbb, rbb, rbf, white))
scene.renderables.append(Triangle(rbf, lbf, lbb, white))

#     # Ceiling
#     scene.renderables.append(Triangle((ltb, ltf, rtf), white))
#     scene.renderables.append(Triangle((rtf, rtb, ltb), white))

# Left wall
scene.renderables.append(Triangle(lbb, lbf, ltf, red))
scene.renderables.append(Triangle(ltf, ltb, lbb, red))

# Right wall
scene.renderables.append(Triangle(rbb, rtb, rtf, green))
scene.renderables.append(Triangle(rtf, rbf, rbb, green))

w = color.WHITE
b = color.BLACK
b1 = color.Material(b, w, b)
b1.diffuse_intensity = .2
b1.specular_intensity = 2.0
b1.specular_hardness = 100

b2 = color.Material(b, b, w)
b2.diffuse_intensity = .2
b2.specular_intensity = 2.0
b2.specular_hardness = 100

scene.renderables.append(Sphere(Point3(150.0,  350.0, 350.0), 100.0, b1))
scene.renderables.append(Sphere(Point3(350.0,  150.0, 150.0), 100.0, b2))


def save_scene(filename):
    import cPickle as pickle
    with open(filename, 'w') as f:
        pickle.dump(scene, f, protocol=0)


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    save_scene(filename)
