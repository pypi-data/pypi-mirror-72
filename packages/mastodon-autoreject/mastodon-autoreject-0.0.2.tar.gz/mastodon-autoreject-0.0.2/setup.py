import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mastodon-autoreject",
    version="0.0.2",
    author="Mark",
    author_email="mark@szy.io",
    description="An automatic follow request rejector for Mastodon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mdszy/autoreject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)