#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="image_analysis_toolbox",
    version="0.0.1-dev",
    description="Core python functions shared between the projects in the lab",
    author=["Andrey Aristov", "Gustave Ronteix"],
    author_email="aaristov@pasteur.fr",
    url="https://gitlab.pasteur.fr/pub/image-analysis",
    install_requires=[
        "numpy",
        "scipy",
        "opencv-python",
        "scikit-image",
        "pims_nd2 @ git+https://github.com/aaristov/pims_nd2.git",
        "nd2reader",
        "pytest",
        "tifffile",
        "tqdm",
        "pandas",
        "seaborn",
        "trackpy"
    ],
    python_requires=">=3.8",
    packages=find_packages(),
)
