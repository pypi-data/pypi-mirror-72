import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opisense_client",
    version="1.5.0",
    author="Patrick Watteyne",
    author_email="pwa@opinum.com",
    description="Package to interact with the Opisense API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/opinum/opisense_client/archive/1.2.0.tar.gz",
    url="https://github.com/opinum/opisense_client",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'requests_oauthlib',
        'oauthlib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
