from setuptools import setup, find_packages


# Function to read the contents of the requirements file
def read_requirements():
    with open('requirements.txt', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
    
    
setup(
    name='breeze-historical-options',
    version='1.1',
    author='Mayank Rai',
    author_email='mrai748@gmail.com',
    description='A Python package for easily downloading historical options data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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