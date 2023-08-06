import setuptools
from setuptools import setup

setup(
    use_incremental=True,
    name="cfdi_admin",
    packages=setuptools.find_packages(),
    scripts=["bin/cfdi-admin"],
    url="http://jorgejuarez.net",
    author="Jorge Juarez",
    author_email="jorgejuarezmx@gmail.com",
    setup_requires=["incremental"],
    install_required=["incremental"]
)