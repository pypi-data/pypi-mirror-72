from setuptools import setup
from distutils.core import setup
setup(
      name="greenviz",
      version="0.0.5",
      description="welcome",
      author="R.raja subramanian",
      url="https://github.com/RRajaSubramanian/Greenviz",
      author_email="rajasubramanian.r1@gmail.com",
      py_modules=["greenviz"],
      package_dir={"":"src"},
      data_files=[("",["shiridi pic rezied.jpeg","bg1.jpg","raja12.jpeg","resized achuth pic.jpeg"])],
      include_package_data=True,
      install_requires=["pillow","matplotlib","sklearn","pandas","numpy","IPython","graphviz"]
      )

