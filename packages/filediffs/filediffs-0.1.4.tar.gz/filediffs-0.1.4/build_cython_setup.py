from distutils.core import setup
from pathlib import Path

from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        [str(Path(__file__).parent / 'filediffs' / 'filediffs_cy.pyx')],
        annotate=False,
        language_level=3),
)

# python build_cython_setup.py build_ext --inplace
