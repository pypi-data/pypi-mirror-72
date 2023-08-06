import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtubepy",
    version="2.5",
    author="toxicrecker",
    author_email="reck.channel.mainlead@gmail.com",
    description="youtubepy is a package to search for youtube videos with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toxicrecker/youtubepy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)