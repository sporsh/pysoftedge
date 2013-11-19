from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Softedge',
  ext_modules = cythonize("softedge/*.py"),
)
