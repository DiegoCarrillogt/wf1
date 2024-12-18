from setuptools import setup, find_packages

setup(
    name="data-processing-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "textblob",
    ],
) 