from setuptools import setup
from distutils.core import setup
setup(
      name="greenviz",
      version="0.0.2",
      description="welcome",
      author="R.raja subramanian",
      url="https://github.com/RRajaSubramanian/Greenviz",
      author_email="rajasubramanian.r1@gmail.com",
      py_modules=["greenviz"],
      include_package_data=True,
      install_requires=["pillow","matplotlib","sklearn","pandas","numpy","IPython","graphviz"],
      package_dir={"":"src"}
      )

