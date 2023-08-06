from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="sirex",
    version="0.0.4",
    description="Simple Regex - A package to use regex commands on strings using simple function calls",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/pythoslabs/sirex",
    author="Pythos Labs",
    author_email="pythoslabs@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["sirex"],
    include_package_data=True,
)






