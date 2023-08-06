from setuptools import setup

from pycrontasks import __version__, __author__, __doc__, __license__


setup(
    name="pycrontasks",
    version=__version__,
    description=__doc__,
    url="https://github.com/dennthecafebabe/pycrontasks",
    author=__author__,
    author_email="dany@cafebabe.date",
    license=__license__,
    packages=["pycrontasks"],
    install_requires=["asyncio", "croniter>=0.3.31"],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
