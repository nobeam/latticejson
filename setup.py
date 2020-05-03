from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup

base_path = Path(__file__).resolve().parent
about: Dict[str, str] = {}
exec((base_path / "latticejson/__about__.py").read_text(), about)
readme = (base_path / "README.md").read_text()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    author=about["__author__"],
    license=about["__license__"],
    packages=find_packages(),
    install_requires=["click>=7.0", "fastjsonschema", "lark-parser", "packaging"],
    test_requires=["pytest"],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"latticejson": ["schema.json", "map.json", "*.lark"]},
    entry_points={"console_scripts": ["latticejson=latticejson.cli:cli"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Scientific/Engineering",
    ],
)
