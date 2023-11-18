import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

with (HERE / "requirements.txt").open() as f:
    requirements = f.read().splitlines()

setup(
    name="growtopiawiki",
    version="1.1",
    description="parse growtopia wiki",
    packages=find_packages(),
    author="zeeetu",
    install_requires=requirements,
)
