import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyManhattan",
    version="0.0.2",
    author="James Han",
    author_email="jamesjisu@gmail.com",
    description="An easy-to-use package to generate Manhattan plots",
    long_description="An easy-to-use package to generate a diverse range of Manhattan plots.",
    long_description_content_type="text/markdown",
    url="https://github.com/jamesjisu/easyManhattan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
