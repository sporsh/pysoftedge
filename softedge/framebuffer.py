import array


class Framebuffer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = array.array('B', (0 for n in xrange(width * height * 3)))

    def set_pixel(self, x, y, color):
        i = ((y * self.width) + x) * 3
        self.buffer[i  ] = max(0, min(255, int(color[0] * 255.0)))
        self.buffer[i+1] = max(0, min(255, int(color[1] * 255.0)))
        self.buffer[i+2] = max(0, min(255, int(color[2] * 255.0)))

    def save(self, filename):
        filename += '.ppm' if not 'filename.'.endswith('.ppm') else ''
        with open(filename, 'wb') as f:
            f.write('P6 %d %d 255\n' % (self.width, self.height))
            self.buffer.tofile(f)
