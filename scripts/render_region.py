import os
import cPickle as pickle
from softedge.color import to_str as color_to_str


def render(filename, fd, sx, sy, sw, sh):
    print "RENDERING REGION x={}, y={}, w={}, h={}".format(sx, sy, sw, sh)
    from softedge.renderer import Sampler

    with open(filename, 'r') as f:
        scene = pickle.load(f)

    sampler = Sampler(scene.geometry, scene.lights)
    for color in sampler.sample(scene.camera, 640, 480, sx, sy, sw, sh):
        os.write(fd, color_to_str(color))


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    filename = args.pop(0)
    fd, sx, sy, sw, sh = (int(arg) for arg in args)
    render(filename, fd, sx, sy, sw, sh)
