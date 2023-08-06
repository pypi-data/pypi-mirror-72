import setuptools

setuptools.setup(
    name = "PyHand_Earth",
    version = "0.0.5",
    author = "PyHandlers",
    description = "Google Earth navigation driven by gesture recognition",
    url = "https://github.com/luijohnj/PyHand_Earth",
    classifiers = [
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(where='PyHand-Earth'),
    package_dir={
        '': 'PyHand-Earth',
    },
    include_package_data=True,
    install_requires=[],

)