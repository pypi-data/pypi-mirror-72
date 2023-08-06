import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymarszpace", # Replace with your own username
    version="1.0.1",
    author="CCSleep",
    author_email="admin@ccsleep.net",
    description="Just a Marszpace package, nothing much.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/CCSleep/pymarszpace/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)