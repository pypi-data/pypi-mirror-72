import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flasker-project",
    version="0.0.1",
    author="Joshua Akangah",
    author_email="joshua@thecodekangaroo.com",
    description="A small package to quickly create a very simple flask project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kangah-codes/flasker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)