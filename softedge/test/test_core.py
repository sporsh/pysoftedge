import unittest
from softedge.core import Vector3, reflect


class TestVector(unittest.TestCase):
    def test_reflect(self):
        A = Vector3(1.0, 1.0, .0)
        normal = Vector3(.0, 1.0, .0)

        self.assertEqual(reflect(A, normal),
                         Vector3(1.0, -1.0, .0))
