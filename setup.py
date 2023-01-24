# based on https://github.com/pypa/sampleproject
# MIT License

from io import open
from os import path

# Always prefer setuptools over distutils
from setuptools import find_namespace_packages
from setuptools import setup

import versioneer

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="asreview-postprocess",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="ASReview postprocesing extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitgarud/asreview-postprocess",
    author="Rohit Garud",
    author_email="rohit.garuda1992@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="asreview postprocess",
    packages=find_namespace_packages(include=["asreviewcontrib.*"]),
    install_requires=[
        "asreview>=1,<2",
        "numpy",
        "scikit-learn",
        "pandas",
        "fuzzywuzzy",
    ],
    extras_require={
        "rake": ["nltk", "rake_nltk"],
        "yake": ["yake @ git+https://github.com/LIAAD/yake"],
        "all": ["nltk", "rake_nltk"],
    },
    entry_points={
        "asreview.entry_points": [
            "keywords = asreviewcontrib.postprocess.entrypoint:KeywordsEntryPoint",
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/rohitgarud/asreview-postprocess/issues",
        "Source": "https://github.com/rohitgarud/asreview-postprocess",
    },
)
