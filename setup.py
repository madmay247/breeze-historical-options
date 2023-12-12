from setuptools import setup, find_packages

# Function to read the contents of the requirements file
def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(
    name='breeze-historical-options',
    version='1.0',
    author='Mayank Rai',
    author_email='mrai748@gmail.com',
    description='A Python package for easily downloading historical options data',
    long_description='A Python package for easily downloading second-level historical options data',
    url='https://github.com/madmay247/breeze-historical-options',
    packages=find_packages(),
    install_requires=read_requirements(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.9',
    )