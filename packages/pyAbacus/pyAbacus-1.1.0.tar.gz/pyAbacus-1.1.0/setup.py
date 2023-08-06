import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyAbacus",
    version="1.1.0",
    author="Juan Barbosa",
    author_email="js.barbosa10@uniandes.edu.co",
    maintainer="David Guzman",
    maintainer_email="da.guzman@outlook.com",
    description=('Build to simplify the usage of Tausands tools.'),
    license="GPL",
    keywords="example documentation tutorial",
    url="https://github.com/Tausand-dev/PyAbacus",
    packages=['pyAbacus'],
    install_requires=['pyserial'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)
