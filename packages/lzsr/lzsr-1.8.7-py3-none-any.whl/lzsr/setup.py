import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lzsr",
    version='1.8.7',
    author="lzsr",
    author_email="y15305083929@outlook.com",
    description="This Python packages can help you simplify some code in programming.",
    long_description='The Python package can undertake some mathematical calculations, and some string encryption and decryption,Can help you to simplify the programming code.',
    long_description_content_type="text/markdown",
    url="https://github.com/lzsr/lzsr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
