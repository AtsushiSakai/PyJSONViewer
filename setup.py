"""


How to upload new release

1. change version in setup.py

2. python setup.py sdist upload

"""
from setuptools import setup, find_packages
from pyjsonviewer import pyjsonviewer

# read README
try:
    import pypandoc
    readme = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    readme = open('README.md').read()

setup(
    name="PyJSONViewer",
    version=pyjsonviewer.VERSION,
    url="https://github.com/AtsushiSakai/PyJSONViewer",
    author="Atsushi Sakai",
    author_email="asakaig@gmail.com",
    maintainer='Atsushi Sakai',
    maintainer_email='asakaig@gmail.com',
    description=("A JSON file data viewer using pure python"),
    long_description=readme,
    python_requires='>3.6.0',
    license="MIT",
    keywords="python json tkinter",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
