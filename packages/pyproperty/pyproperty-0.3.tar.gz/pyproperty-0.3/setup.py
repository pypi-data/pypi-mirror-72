import setuptools

with open("README.md") as ld:
    long_description = ld.read()

setuptools.setup(
    name = "pyproperty",
    version = "0.3",
    author = "raifpy",
    author_email = "omerto12.45y@gmail.com",
    description="Python Explore Modules Func Tool *",
    long_description=long_description,
    url = "https://github.com/raifpy/pyproperty",
    packages=setuptools.find_packages(),
    install_requires = ["colorama"],
    python_requires= ">=3.5",
    scripts = ["pyproperty/pyproperty"]
        )
