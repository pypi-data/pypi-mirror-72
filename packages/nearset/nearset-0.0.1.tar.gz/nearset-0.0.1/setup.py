import numpy
import setuptools
from Cython.Build import cythonize
from setuptools import Extension


extensions = [
    Extension("nearset/*", ["nearset/*.pyx"]),
]

setuptools.setup(
    name="nearset",
    version="0.0.1",
    author="Maixent Chenebaux",
    author_email="max.chbx@gmail.com",
    description="Efficient ordered set of elements with custom comparator function in Python",
    long_description_content_type="text/markdown",
    url="https://github.com/kerighan/nearset",
    packages=setuptools.find_packages(),
    include_path = [numpy.get_include()],
    include_package_data=True,
    ext_modules=cythonize(extensions),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5"
)
