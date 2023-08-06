import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ClockworkOrange",
    version="0.0.1",
    author="Yixiao Lan",
    author_email="yixiaolan@foxmail.com",
    description="A lightweight digital circuit simulation package for humans.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eathoublu/ClockWorkOrange",
    # packages=setuptools.find_packages(),
    packages=['ClockworkOrange', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
)


