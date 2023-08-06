import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pcdm", # Replace with your own username
    version="0.0.1",
    author="Gene Dan",
    author_email="genedan@gmail.com",
    description="Property Casualty Data Model Standard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/genedan/pcdm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.8',
)
