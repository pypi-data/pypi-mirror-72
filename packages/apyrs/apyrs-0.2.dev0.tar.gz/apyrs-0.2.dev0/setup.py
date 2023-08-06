from os import path

from setuptools import find_packages
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name="apyrs",
    version="0.2dev0",
    packages=find_packages(exclude=['docs']),
    install_requires=install_requires,
    author="Iain R. Learmonth",
    author_email="irl@hambsd.org",
    description=("APRS for Python"),
    long_description=long_description,
    keywords="aprs local hamradio packet kiss",
    classifiers=["License :: OSI Approved :: BSD License"],
    test_suite='nose.collector',
)
