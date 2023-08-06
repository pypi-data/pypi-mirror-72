import setuptools
from setuptools import setup


setup(
    name = "NetView",
    version = 0.4,
    packages= setuptools.find_packages(),
    description='Network Grapher',
    install_requires=["networkx","Django","matplotlib"],

    entry_points =
    { 'console_scripts':
        [
            'runmyserver = sample.run:main',
            'initmigrate = sample.init:main',
        ]
    },
)