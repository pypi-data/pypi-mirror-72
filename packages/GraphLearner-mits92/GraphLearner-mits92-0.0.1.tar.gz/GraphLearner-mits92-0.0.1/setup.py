import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GraphLearner-mits92", # Replace with your own username
    version="0.0.1",
    author="Preston Ward",
    author_email="preston.ward@go.tarleton.edu",
    description="To help make working with graphs easier to develop intuition.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'networkx',
          'matplotlib',
      ],
    python_requires='>=3.6',
)