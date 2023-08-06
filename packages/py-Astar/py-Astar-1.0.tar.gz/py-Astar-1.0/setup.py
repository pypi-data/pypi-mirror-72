import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-Astar", 
    version="1.0",
    author="Adwait Naik",
    author_email="adwaitnaik2@gmail.com",
    description="Implementation of Astar algorithm in python using matplotlib.",
    long_description="Astar is an algorithm based on heuristics for finding shortest collision-free path between two points.",
    long_description_content_type="text/markdown",
    url="https://github.com/addy1997/py-Astar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
