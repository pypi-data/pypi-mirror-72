import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datetime-selenium",
    version="0.0.0",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="Send and receive datetime objects from web forms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dsbowen.github.io/datetime-selenium",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['selenium>=3.141.0']
)