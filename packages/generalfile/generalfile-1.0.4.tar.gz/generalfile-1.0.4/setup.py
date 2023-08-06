
from setuptools import setup, find_packages

from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="generalfile",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Rickard "Mandera" Abraham',
    url="https://github.com/Mandera/generalfile",
    version="1.0.4",
    description=(
        "Easily manage windows files."
    ),
    packages=find_packages(),
    install_requires=["generallibrary", "send2trash", "pandas", "wheel"],
    classifiers=[
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Desktop Environment :: File Managers",
    ]
)
