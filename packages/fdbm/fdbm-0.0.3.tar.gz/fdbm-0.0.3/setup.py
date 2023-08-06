import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fdbm",
    version="0.0.3",
    author="Ibrahim Abbas",
    author_email="i.abbas85@gmail.com",
    description="File data base system used to save/update/delete/find class objects to files easly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IbrahimABBAS85/fdb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pathlib",
        "mexp",
        "jsonpickle",
        "jpfmanager"
    ],
)