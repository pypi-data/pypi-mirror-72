import setuptools
from setuptools import Extension


extensions = [
    Extension("nearset", sources=["nearset/__init__.c"]),
    Extension("nearset/metrics", sources=["nearset/metrics.c"]),
]

setuptools.setup(
    name="nearset",
    version="0.0.3",
    author="Maixent Chenebaux",
    author_email="max.chbx@gmail.com",
    description="Efficient ordered set of elements with custom comparator function in Python",
    long_description_content_type="text/markdown",
    url="https://github.com/kerighan/nearset",
    packages=setuptools.find_packages(),
    include_package_data=True,
    ext_modules=extensions,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5"
)
