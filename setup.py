from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='FileTransforms',
    version='0.1',
    description='A library for easily transforming files',
    url='http://github.com/kallam/FileTransforms',
    author='Alex Kallam',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['csvkit'],
    extras_require={
        'dev': ['pytest']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
