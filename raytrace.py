from softedge.renderer import RaytraceRenderer
from softedge.core import Scene, Light, Camera, Sphere, Triangle, Point3, Vector3
from softedge import color


def main():
    scene = Scene(color.GRAY, ambient=.5)
    scene.lights.append(Light(Point3(20.0, 120.0, 100.0), .8))
    scene.lights.append(Light(Point3(700.0, .0, .0), .4))
    scene.renderables.append(Sphere(Point3(320.0, 240.0, 400.0), 200.0, color.YELLOW))
    scene.renderables.append(Sphere(Point3(450.0, 200.0, 220.0), 40.0, color.RED))
    scene.renderables.append(Sphere(Point3(230.0, 350.0, 320.0), 100.0, color.GREEN))
    scene.renderables.append(Sphere(Point3(500.0, 400.0, 500.0), 250.0, color.BLUE))

    scene.renderables.append(Triangle((
                                       Point3(100.0, 50.0, 600.0),
                                       Point3(100.0, 400.0, 400.0),
                                       Point3(400.0, 100.0, 100.0),
                                       ), color.WHITE))
    scene.renderables.append(Triangle((
                                       Point3(100.0, 400.0, 400.0),
                                       Point3(200.0, 550.0, 800.0),
                                       Point3(400.0, 100.0, 100.0),
                                       ), color.WHITE))

    camera = Camera(Point3(320.0, 240.0, .0), Vector3(.0, .0, 1.0))

    renderer = RaytraceRenderer(640, 480)
    renderer.render(scene, camera)


if __name__ == '__main__':
    main()
