import setuptools

with open ("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nester-Mark_Challender",
    version="0.0.1",
    author="Mark Challender",
    author_email="mark@challenderltd.co.uk",
    description="A simple printer of nested lists",
    long_description=long_description,
    packages=setuptools.find_packages(),
    )
