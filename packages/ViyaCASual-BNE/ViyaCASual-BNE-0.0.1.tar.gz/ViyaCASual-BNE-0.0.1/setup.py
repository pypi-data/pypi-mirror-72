import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ViyaCASual-BNE",
    version="0.0.1",
    author="Will Haley",
    author_email='willhaley@boddienoell.com',
    descripton='A simple way to use Viya\'s tools in Python without getting too serious',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/willhaley-bne/ViyaCasual",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
