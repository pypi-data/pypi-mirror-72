"""
tablite
"""
build_tag = "58e698fca228c2e61b88c64d46ae5766aae8cf759e56d3e3a9dd0888798b53f1"
from setuptools import setup
from pathlib import Path


folder = Path(__file__).parent
file = "README.md"
readme = folder / file
assert isinstance(readme, Path)
assert readme.exists(), readme
with open(str(readme), encoding='utf-8') as f:
    long_description = f.read()

keywords = list({
    'tables'
})

keywords.sort(key=lambda x: x.lower())


setup(
    name="tablite",
    version="2020.6.28.62006",
    url="https://github.com/root-11/tablite",
    license="MIT",
    author="Bjorn Madsen",
    author_email="bjorn.madsen@operationsresearchgroup.com",
    description="A table crunching library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=keywords,
    packages=["table"],
    include_package_data=True,
    data_files=[(".", ["LICENSE", "README.md"])],
    platforms="any",
    install_requires=[
        'xlrd>=1.2.0',
        'pyexcel-ods>=0.5.6'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)


