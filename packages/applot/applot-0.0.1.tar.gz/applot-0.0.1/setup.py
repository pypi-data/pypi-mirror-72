import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="applot", # Replace with your own username
    version="0.0.1",
    author="Austin Poor",
    author_email="austinpoor@gmail.com",
    description="A small svg plotting library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-poor/applot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
