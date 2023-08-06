import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="varq-py",
    version="0.1.5",
    author="Mauro Song",
    author_email="tik@lag.party",
    description="VarQ API wrapper for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/glyco1/varq-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    python_requires=">=3.7",
)
