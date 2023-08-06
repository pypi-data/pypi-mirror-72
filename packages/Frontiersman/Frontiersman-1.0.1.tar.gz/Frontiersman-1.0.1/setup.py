import io
from setuptools import setup, find_packages

setup(
    name="Frontiersman",
    version="1.0.1",
    author="Brian Snow",
    author_email="snowb@ufl.edu",
    description="Network Multiplayer Board Game",
    install_requires=['pygame>=2.0.0.dev10', 'pygame_gui'],
    long_description=io.open(
        './README.md', 'r', encoding='utf-8').read(),
    url="https://github.com/ForgedSnow/Frontiersman",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'FMClient = Frontiersman.ClientMain:main',
            'FMServer = Frontiersman.server:main'
        ],
    }
)