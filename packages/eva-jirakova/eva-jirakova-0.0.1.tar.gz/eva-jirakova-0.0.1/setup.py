import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eva-jirakova",
    version="0.0.1",
    author="Katerina Hromasova",
    author_email="jirakova@ipp.cas.cz",
    description="EVA (Equation Visualisation Applet) displays and interlinks a set of equations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://repo.tok.ipp.cas.cz/jirakova/eva",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
        'xarray',
    ],
)
