from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="scrapybase",
    packages=['base_scrapy_project',],
    version="1.0.0",
    author="Cisco Delgado",
    author_email="fdelgados@gmail.com",
    description="Base Scrapy project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fdelgados/ScrapyBase.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3',
    install_requires=['pymongo', 'scrapy']
)
