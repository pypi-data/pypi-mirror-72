import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test_stratergy", # Replace with your own username
    version="0.0.1",
    author="Harshit Agarwal",
    author_email="9arshit@gmail.com",
    description="This package is used to test you trading stragey integrated with deep learning models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/9harshit/trading_stratergy_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',


    
)
