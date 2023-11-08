from setuptools import find_packages, setup

setup(
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
)
