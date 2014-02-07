from softedge import color
from softedge.renderer import Sampler


def main(out_filename='rtr_scene_camera.pam'):
    from scripts.create_scene import Scene

    width, height = 640, 480
    sampler = Sampler(Scene.geometry, Scene.lights)
    with open(out_filename, 'wb') as f:
        f.write('P7\n'
                'WIDTH %d\n'
                'HEIGHT %d\n'
                'DEPTH 4\n'
                'MAXVAL 255\n'
                'TUPLTYPE RGB_ALPHA\n'
                'ENDHDR\n' % (width, height))
        for color_ in sampler.sample(Scene.camera, width, height, 0, 0, width, height):
            f.write(color.to_str(color_))


if __name__ == '__main__':
    main()
