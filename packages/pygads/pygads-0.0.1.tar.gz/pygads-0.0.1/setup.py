import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygads",
    version="0.0.1",
    author="Dacker",
    author_email="hello@dacker.co",
    description="A Google Ads connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dacker-team/pygads",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        "dbstream>=0.0.16",
        "googleauthentication",
    ],
)
