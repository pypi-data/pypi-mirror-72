import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thaifortrading",
    version="0.0.5",
    author="Chayaphon Tanwongvarl",
    author_email="chayaphont@yahoo.co.uk",
    description="Collections of Thai for trading codes",
    long_description="Collections of Thai for trading codes",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=['numpy'],
)
