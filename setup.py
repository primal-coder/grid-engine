from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()
    
setup(
    name='gridengine_framework',
    version='0.3.0',
    description='A framework for generating and manipulating grid-based game worlds',
    long_description=long_description,
    long_description_content_type="text/markdown",
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