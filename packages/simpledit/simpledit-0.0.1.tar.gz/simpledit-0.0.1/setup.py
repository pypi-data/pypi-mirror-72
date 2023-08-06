from setuptools import setup, find_packages

setup(
    name='simpledit',
    version='0.0.1',
    url='https://gitlab.com/torresed/simpledit',
    author='Edilberto Torres',
    author_email='torrese@ufl.edu',
    description='A simple image editor',
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "PyQt5",
        "PyQt5-sip",
    ],
)
