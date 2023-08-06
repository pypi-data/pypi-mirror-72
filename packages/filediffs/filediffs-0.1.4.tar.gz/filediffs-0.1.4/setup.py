import os

from Cython.Build import cythonize
from Cython.Distutils.build_ext import new_build_ext
from setuptools import Extension, setup


def read(f):
    """Open a file"""
    return open(f, encoding='utf-8').read()


setup(
    name='filediffs',
    version='0.1.4',
    include_package_data=True,
    description="Separate two files into three files, each containing "
                "lines observed in both files/first file only/second file only. Programmed using Cython.",
    long_description=read('README.md'),
    author='Sebastian Cattes',
    author_email='sebastian.cattes@inwt-statistics.de',
    long_description_content_type="text/markdown",
    url='https://github.com/INWTlab/filediffs',
    package_data={'filediffs': [os.path.join(os.path.dirname(__file__), 'filediffs', "filediffs_cy.pyx"),
                                os.path.join(os.path.dirname(__file__), 'filediffs', "filediffs.py"),
                                os.path.join(os.path.dirname(__file__), 'filediffs', "filediffs_script.py")]},
    extensions=[Extension("filediffs",
                          [os.path.join(os.path.dirname(__file__), 'filediffs', "filediffs_cy.pyx")])
                ],
    ext_modules=cythonize(Extension("filediffs",
                                    [os.path.join(os.path.dirname(__file__), 'filediffs', "filediffs_cy.pyx")])
                          ),
    cmdclass={'build_ext': new_build_ext},
    entry_points={
        'console_scripts': ['filediffs=filediffs.filediffs_script:main'],
    },
    requires=['cython'],
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8',
    ),
)
