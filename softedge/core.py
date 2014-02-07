class Light(object):
    def __init__(self, origin, color, intensity=1.0):
        self.origin = origin
        self.radiance = color * intensity

    def get_illumination(self, point):
        """Get illumination details for a specific spatial point
        """
        direction = (self.origin - point).normalize()
        return direction, self.intensity


class Camera(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
