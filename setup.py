import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discord-cli",
    version="1.0.0",
    author="Kieran Powell",
    author_email="kieranleep@hotmail.com",
    description="A simple command line interface for discord bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kappeh/discord-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)