from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="kafka-broker",
    version="0.0.7",
    description="A python package implementation for the confluent kafka package. Managing producing and consuming.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TijmenSimons/kafka-broker",
    author="Tijmen Simons, Ivar Stek",
    author_email="tijmen.simons@student.hu.nl, ivar.stek@student.hu.nl",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["confluent_kafka >= 2.3.0"],  # "bson >= 0.5.10"
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.11",
)
