from softedge.renderer import RaytraceRenderer
from softedge.core import Scene, Light, Camera, Sphere, Triangle, Point3, Vector3
from softedge import color


def main():
    scene = Scene(color.BLACK, ambient=.2)
    scene.lights.append(Light(Point3(-500.0, -500.0, -1000.0), 1.0))
    scene.lights.append(Light(Point3(75.0, 25.0, -350.0), 1.0))

    white = color.Color(.8, .8, .8)
    red = color.Color(.8, .5, .5)
    green = color.Color(.5, .8, .5)
    blue = color.Color(.5, .5, .8)

    scene.renderables.append(Sphere(Point3(-200.0, -200.0, 200.0), 100.0, red))
    scene.renderables.append(Sphere(Point3(.0,     -200.0, .0), 100.0, green))
    scene.renderables.append(Sphere(Point3(200.0,  -200.0, 200.0), 100.0, blue))

    scene.renderables.append(Sphere(Point3(-200.0, .0,     .0), 100.0, green))
    scene.renderables.append(Sphere(Point3(.0,     .0,     200.0), 250.0, white))
    scene.renderables.append(Sphere(Point3(200.0,  .0,     .0), 100.0, red))

    scene.renderables.append(Sphere(Point3(-200.0, 200.0, 200.0), 100.0, blue))
    scene.renderables.append(Sphere(Point3(.0,     200.0, .0), 100.0, red))
    scene.renderables.append(Sphere(Point3(200.0,  200.0, 200.0), 100.0, green))


#     c = Point3(.0, .0, .0)
#     tl = Point3(-100.0, 100.0, 100.0)
#     tr = Point3(100.0, 100.0, 100.0)
#     bl = Point3(-100.0, -100.0, 100.0)
#     br = Point3(100.0, -100.0, 100.0)
#     scene.renderables.append(Triangle((c, tl, tr), color.WHITE))
#     scene.renderables.append(Triangle((c, tr, br), color.WHITE))
#     scene.renderables.append(Triangle((c, bl, br), color.WHITE))
#     scene.renderables.append(Triangle((c, bl, tl), color.WHITE))

# ------

#     scene.renderables.append(Sphere(Point3(320.0, 240.0, 400.0), 200.0, color.YELLOW))
#     scene.renderables.append(Sphere(Point3(450.0, 200.0, 220.0), 40.0, color.RED))
#     scene.renderables.append(Sphere(Point3(230.0, 350.0, 320.0), 100.0, color.GREEN))
#     scene.renderables.append(Sphere(Point3(500.0, 400.0, 500.0), 250.0, color.BLUE))
# 
#     scene.renderables.append(Triangle((
#                                        Point3(100.0, 50.0, 600.0),
#                                        Point3(100.0, 400.0, 400.0),
#                                        Point3(400.0, 100.0, 100.0),
#                                        ), color.WHITE))
#     scene.renderables.append(Triangle((
#                                        Point3(100.0, 400.0, 400.0),
#                                        Point3(200.0, 550.0, 800.0),
#                                        Point3(400.0, 100.0, 100.0),
#                                        ), color.WHITE))

# ------

#     scene.renderables.append(Sphere(Point3(-150.0, .0, .0), 100.0, color.RED))
#     scene.renderables.append(Sphere(Point3(.0, .0, .0), 100.0, color.GREEN))
#     scene.renderables.append(Sphere(Point3(150.0, .0, .0), 100.0, color.BLUE))

    camera = Camera(Point3(.0, .0, -1000.0), Vector3.Z)

    renderer = RaytraceRenderer(640, 480)
    renderer.render(scene, camera)


if __name__ == '__main__':
    main()
