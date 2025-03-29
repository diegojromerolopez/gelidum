import os
from setuptools import setup, find_packages

root_dir_path = os.path.dirname(os.path.abspath(__file__))

long_description = open(os.path.join(root_dir_path, "README.md")).read()

setup(
    name="gelidum",
    version="0.7.2",
    author="Diego J. Romero López",
    author_email="diegojromerolopez@gmail.com",
    description="Freeze your python objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[],
    license="MIT",
    keywords="freeze python object",
    url="https://github.com/diegojromerolopez/gelidum",
    packages=find_packages(),
    data_files=[],
    include_package_data=True,
    scripts=[]
)
