#!/usr/bin/env python
import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"([^"]*)"',
    open("suplemon/main.py").read(),
    re.M
    ).group(1)

files = ["config/*.json", "themes/*", "modules/*.py", "linelight/*.py"]

setup(name="Suplemon",
      version=version,
      description="Console text editor with multi cursor support.",
      author="Richard Lewis",
      author_email="richrd.lewis@gmail.com",
      url="https://github.com/richrd/suplemon/",
      packages=["suplemon"],
      package_data={"": files},
      include_package_data=True,
      install_requires=[
          "pygments",
          "wcwidth"
      ],
      entry_points={
          "console_scripts": ["suplemon=suplemon.cli:main"]
      },
      classifiers=[]
      )
