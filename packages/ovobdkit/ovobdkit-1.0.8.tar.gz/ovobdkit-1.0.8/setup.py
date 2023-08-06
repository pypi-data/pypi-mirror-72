import setuptools
from bash import bash

ver_str = bash('git describe --tags $(git rev-list --tags --max-count=1)')
branch_str = bash('git rev-parse --abbrev-ref HEAD')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ovobdkit", # Replace with your own username
    version=f'{ver_str}',
    author="OVO BD Enginners, Zaky Rahim",
    author_email="bd-engineers@ovo.id, zaky.rahim@ovo.id",
    description="Big Data Development Kit for OVO Big Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'psycopg2-binary',
        'pandas',
        'pyspark',
        'bash',
        'sqlalchemy'
    ],
    python_requires='>=3.6',
)