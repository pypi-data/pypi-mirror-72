from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='txnet',
    version='0.1',
    author='Anmol Gautam',
    packages=['txnet'],
    install_requires=[
        'numpy',
    ],
    description='Keras inspired pure python neural network library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Tarptaeya/txnet',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
