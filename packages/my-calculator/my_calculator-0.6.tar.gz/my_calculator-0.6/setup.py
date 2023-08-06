from __future__ import absolute_import, division, print_function
import os
from setuptools import setup

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

setup(name = "my_calculator",
      version = "0.6",
      description = "Several calculations of two numbers",
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages = ["my_calculator"],
      author = "Adarsh Ghimire",
      email = "adarsh.ghimire1@gmail.com",
      url= "https://github.com/ghimireadarsh/My-Calculator.git",
      zip_safe = False)