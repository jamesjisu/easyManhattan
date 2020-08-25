import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyManhattan",
<<<<<<< HEAD
    version="0.0.3",
=======
    version="0.0.2",
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a
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
