import setuptools
import os
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zwack",
    version="2.1.0",
    author="codemonkey51",
    author_email='pypi@codemonkey51.dev',
    description="zwackkk",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="",
    install_requires=[
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)