from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="locatorpoint",
    version="1.0.0",
    description="Python Package to get the information from Geo Coordinates",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mandiladitya",
    author="Aditya Mandil",
    author_email="adityamandil317@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["geo_sight"],
    include_package_data=True,
    install_requires=["requests","geopy","wolframalpha"],
    entry_points={
        "console_scripts": [
            "geo-locate=geo_sight.cli:main",
        ]
    },
)
