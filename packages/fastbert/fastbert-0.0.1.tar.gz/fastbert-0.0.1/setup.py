import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="fastbert", # Replace with your own username
    version="0.0.1",
    author="Weijie Liu",
    author_email="autoliuweijie@example.com",
    description="The pipy version of FastBERT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/autoliuweijie/FastBERT_pypi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
