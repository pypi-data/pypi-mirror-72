import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tf-stitch", 
    version="1.0.0",
    author="Hemant Singh",
    keywords="deep learning , Boilerplate , Starter Code , Starter Pieces , Quick Work , Productivity",
    description="Quick Starter Code with different specifications stitched together.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amifunny/tf-stitch/",
    maintainer="amifunny",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)