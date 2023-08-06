import setuptools
from setuptools import setup


setup(
    name = "NetView",
    version = 0.3,
    packages= setuptools.find_packages(),
    description='Network Grapher',
    install_requires=["networkx","Django","matplotlib"],

    entry_points =
    { 'console_scripts':
        [
            'runmyserver = src.sample.run:main'
            'initmigrate = src.sample.init:main'
        ]
    },
)