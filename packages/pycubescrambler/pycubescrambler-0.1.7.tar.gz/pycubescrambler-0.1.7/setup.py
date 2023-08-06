import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycubescrambler", # Replace with your own username
    version="0.1.7",
    author="Example Author",
    author_email="midnightcuberx@gmail.com",
    description="A scrambling package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/midnightcuberx/pycubescrambler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
