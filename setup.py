from setuptools import setup, find_packages

setup(
    name='gridengine_framework',
    version='0.2.0',
    description='A framework for generating and manipulating grid-based game worlds',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    url='https://github.com/primal-coder/grid-engine',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow',
        'pyglet',
        'pymunk',
        'noise'
    ],
    keywords='game development 2d grid world generation procedural generation cell numpy pillow pyglet pymunk cli',
    include_package_data=True,
    package_data={'grid_engine': ['_blueprint/terrains.json']}

)