import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
def _requires_from_file(filename):
    return open(filename).read().splitlines()

setuptools.setup(
    name="fnbot",
    version="0.1.0",
    author="HRTK92",
    author_email="　",
    description="You can receive the message 'Hello!!!'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HRTK92/fnbot/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
    },
    python_requires='>=3.7',
    install_requires=_requires_from_file("requirements.txt")
)
