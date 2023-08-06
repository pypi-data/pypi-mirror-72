import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='anonfile',
    version='0.1.2',
    author="Nicholas Strydom",
    author_email="nstrydom@gmail.com",
    description="An unofficial library that wraps the Anonfile.com REST Api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nstrydom2/anonfile-api",
    packages=setuptools.find_packages(exclude=['tests*']),
    python_requires='>=3.7',
    install_requires=[
        'beautifulsoup4>=4.9.0',
        'bs4>=0.0.1',
        'certifi>=2020.4.5.1',
        'chardet>=3.0.4',
        'hurry.filesize>=0.9',
        'idna>=2.9',
        'lxml>=4.5.0',
        'python3-wget>=0.0.2b1',
        'requests>=2.23.0',
        'soupsieve>=2.0',
        'urllib3>=1.25.8'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
