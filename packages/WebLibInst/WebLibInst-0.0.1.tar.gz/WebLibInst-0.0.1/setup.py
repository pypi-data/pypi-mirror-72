import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WebLibInst",
    version="0.0.1",
    author="dirt3009",
    author_email="emirgecir5@gmail.com",
    description="A library that wraps Instagram's web API",
    url="https://github.com/dirt3009/WebLibInst",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)