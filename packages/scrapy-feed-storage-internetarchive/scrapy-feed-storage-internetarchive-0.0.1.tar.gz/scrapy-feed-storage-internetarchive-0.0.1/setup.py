import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-feed-storage-internetarchive",
    version="0.0.1",
    author="JD Bothma",
    author_email="jd@openup.org.za",
    description="Scrapy Item Feed Storage Backend for archive.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenUpSA/scrapy-feed-storage-internetarchive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'internetarchive',
    ],
)
