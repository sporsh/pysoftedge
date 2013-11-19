import os
from softedge.color import to_str as color_to_str

def render(fd, sx, sy, sw, sh):
    print "RENDERING REGION x={}, y={}, w={}, h={}".format(sx, sy, sw, sh)
    from softedge.renderer import RaytraceRenderer
    from softedge.core import Camera, Point3, Vector3 

    import cPickle as pickle
    with open('scene.pickle', 'r') as f:
        scene = pickle.load(f)

    camera = Camera(Point3(250.0, 250.0, -800.0), Vector3.Z)
    renderer = RaytraceRenderer(640, 480)
    for color in renderer.render_region(scene, camera, sx, sy, sw, sh):
        os.write(fd, color_to_str(color))


if __name__ == '__main__':
    import sys
    fd, sx, sy, sw, sh = (int(arg) for arg in sys.argv[1:])
    render(fd, sx, sy, sw, sh)
