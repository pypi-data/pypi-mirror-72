import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ovotestkit", # Replace with your own username
    version="1.0.0",
    author="OVO BD Enginners, Zaky Rahim",
    author_email="bd-engineers@ovo.id, zaky.rahim@ovo.id",
    description="Testing Kit for OVO Big Data",
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