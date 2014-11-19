# chardet's setup.py
from distutils.core import setup
setup(
    name = "topogram",
    packages = ["topogram"],
    version = "0.0.1",
    description = "Network Analysis",
    author = "Clement Renaud",
    author_email = "clement.renaud@gmail.com",
    url = "http://topogram.io",
    download_url = "http://github.com/topogram/topogram",
    keywords = ["network", "visualization", "NLP"],
    classifiers = [
        "Programming Language :: Python",
        "Environment :: Other Environment",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        ],
    long_description = open('README.txt').read()
    )

