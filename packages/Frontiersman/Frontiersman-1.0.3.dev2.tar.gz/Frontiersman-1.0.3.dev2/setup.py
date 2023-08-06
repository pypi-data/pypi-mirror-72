import io
from setuptools import setup, find_packages

setup(
    name="Frontiersman",
    version="1.0.3.dev2",
    author="Brian Snow",
    author_email="snowb@ufl.edu",
    description="Network Multiplayer Board Game",
    install_requires=['pygame>=2.0.0.dev10', 'pygame_gui'],
    long_description=io.open(
        './README.md', 'r', encoding='utf-8').read(),
    url="https://github.com/ForgedSnow/Frontiersman",
    packages=find_packages(),
    include_package_data = True,
    package_data={
        'frontiersman': ['assets/*.png'],
        'frontiersman': ['assets/cards/dev/*.png'],
        'frontiersman': ['assets/cards/res/*.png'],
        'frontiersman': ['assets/cards/vic/*.png'],
        'frontiersman': ['assets/cards/*.png'],
        'frontiersman': ['assets/hexes/*.png'],
        'frontiersman': ['assets/Pieces/Cities/*.png'],
        'frontiersman': ['assets/Pieces/Miscellaneous/*.png'],
        'frontiersman': ['assets/Pieces/Resource Numbers/*.png'],
        'frontiersman': ['assets/Pieces/Roads/*.png'],
        'frontiersman': ['assets/Pieces/Settlements/*.png'],
        'frontiersman': ['assets/scaled/*.png']
        },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'FMClient = frontiersman.ClientMain:main',
            'FMServer = frontiersman.server:main'
        ],
    }
)