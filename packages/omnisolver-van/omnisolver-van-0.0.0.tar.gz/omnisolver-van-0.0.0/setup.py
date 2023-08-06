"""Setup script for omnisolver-van project."""
from setuptools import setup, find_namespace_packages

with open("README.md") as readme:
    long_description = readme.read()


setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    name="omnisolver-van",
    entry_points={
        "omnisolver": ["random = omnisolver.random"]
    },
    install_requires=["omnisolver", "dimod", "numpy>=1.17.0", "pluggy", "torch"],
    tests_require=["pytest"],
    packages=find_namespace_packages(exclude=["tests"]),
    package_data={"omnisolver.van": ["van.yml"]},
)
