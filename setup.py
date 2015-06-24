# chardet's setup.py
from setuptools import setup,find_packages

setup(
      name = "topogram",
      packages = find_packages(exclude=['tests']) ,
      version = "0.0.2",
      description = "Network Analysis",
      author = "Clement Renaud",
      author_email = "clement.renaud@gmail.com",
      url = "http://topogram.io",
      download_url = "http://github.com/topogram/topogram",
      include_package_data=True,
      keywords = ["network", "visualization", "NLP"],
      entry_points={
        'console_scripts': [
            # 'topo-test = topogram.cli:main',
            'topo-viz = topogram.cli:topo_viz_main',
            'topo-proc = topogram.cli:topo_proc_main',
            'topo-corpus = topogram.cli:topo_corpus_main',
        ],
    },
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
      long_description = open('README.md').read(),
      install_requires=[
      'networkx',
      "jieba",
      "chardet",
      "python-dateutil",
      "pymongo"
      ],
      test_suite='tests'
      )

