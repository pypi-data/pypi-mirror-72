import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="e6b",
    version="0.0.1",
    author="Andrew Trail",
    author_email="andrewtrail@googlemail.com",
    description="A simple e6b flight calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DessyT/E6B",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
