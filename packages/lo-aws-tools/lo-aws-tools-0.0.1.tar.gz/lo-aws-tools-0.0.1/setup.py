import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lo-aws-tools",
    version="0.0.1",
    author="Dyllan Pascoe",
    author_email="dyllan@lookopen.com",
    description="AWS Python API custom tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dyllan/lo-aws-tools",
    install_requires=['boto3'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
