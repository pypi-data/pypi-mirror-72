import setuptools
from pathlib import Path

setuptools.setup(
    name="sergiopdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packeges=setuptools.find_packages(exclude=["tests", "data"])
)
