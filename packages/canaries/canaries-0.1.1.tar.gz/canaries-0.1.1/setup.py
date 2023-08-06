from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="canaries",
    version="0.1.1",
    packages=["canaries",],
    install_requires=[],
    license="MIT",
    url="https://github.com/reity/canaries",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Python library for choosing and loading dynamic library " +\
                "files compatible with the operating environment.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
