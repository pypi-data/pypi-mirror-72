import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bazeler",
    version="0.0.11",
    author="Ian Baldwin",
    author_email="ian@iabaldwin.com",
    description="Bazel helper package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iabaldwin/bazeler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['bazeler=bazeler.command_line:main'],
    },
    include_package_data = True,
    install_requires = ['jinja2', 'colorama'],
    python_requires = '>=3.6',
)
