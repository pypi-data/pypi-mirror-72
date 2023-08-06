from os import path
from codecs import open
from setuptools import setup, find_packages
from rosey_deprecated import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='rosey-deprecated',
    version=__version__,
    description='Quickly deprecated functions, methods and classes',
    url='https://github.com/arose13/rosey-deprecated',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(),
    author='Stephen Rose',
    author_email='me@stephenro.se',
    zip_safe=False
)
