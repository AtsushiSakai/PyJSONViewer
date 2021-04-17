"""

Setup script for PyJSONViewer

How to upload new release

1. run bum-version.sh

2. setup twine, see:https://blog.amedama.jp/entry/2017/12/31/175036

3. create zip file: python setup.py sdist

4. upload: twine upload --repository pypi dist/PyJSONViewer-1.3.0.tar.gz

twine check dist/pyroombaadapter-0.1.2.tar.gz
twine upload --repository pypitest dist/pyroombaadapter-0.1.8.tar.gz
pip install --upgrade -i https://test.pypi.org/simple/ pyroombaadapter
"""
from setuptools import setup, find_packages
import os
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# read README
try:
    import pypandoc
    readme = pypandoc.convert_file(PROJECT_PATH + '/README.md', 'rst')
except(IOError, ImportError):
    readme = open(PROJECT_PATH + '/README.md').read()

# read VERSION
with open(PROJECT_PATH + "/pyjsonviewer/VERSION", 'r') as fd:
    VERSION = fd.readline().rstrip('\n')

setup(
    name="PyJSONViewer",
    version=VERSION,
    url="https://github.com/AtsushiSakai/PyJSONViewer",
    author="Atsushi Sakai",
    author_email="asakaig@gmail.com",
    maintainer='Atsushi Sakai',
    maintainer_email='asakaig@gmail.com',
    description="A JSON file data viewer using pure python",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>3.6.0',
    license="MIT",
    keywords="python json tkinter",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['pyjsonviewer=pyjsonviewer.pyjsonviewer:main']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
