import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent

setuptools.setup(
    name = "PyHand_Earth",
    version = "0.0.9",
    description = "Google Earth navigation driven by gesture recognition",
    url = "https://github.com/luijohnj/PyHand_Earth",
    classifiers = [
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    

)