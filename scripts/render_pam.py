from softedge import color
from softedge.core import Camera, Point3, Vector3
from softedge.renderer import RaytraceRenderer


def main(out_filename='rtr_scene_camera.pam'):
    from scripts.create_scene import scene
    camera = Camera(Point3(250.0, 250.0, -800.0), Vector3.Z)

    width, height = 640, 480
    renderer = RaytraceRenderer(width, height)
    with open(out_filename, 'wb') as f:
        f.write('P7\n'
                'WIDTH %d\n'
                'HEIGHT %d\n'
                'DEPTH 4\n'
                'MAXVAL 255\n'
                'TUPLTYPE RGB_ALPHA\n'
                'ENDHDR\n' % (width, height))
        for color_ in renderer.render_region(scene, camera, 0, 0, width, height):
            f.write(color.to_str(color_))


if __name__ == '__main__':
    main()
