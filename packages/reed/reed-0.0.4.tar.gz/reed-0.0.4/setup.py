import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reed",
    version="0.0.4",
    author="Theo Rutter",
    author_email="theo.rutter@gmail.com",
    description="Search for jobs using the Reed API in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theo-r/reed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
