from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mediapart_parser',
    packages=['mediapart_parser'],
    version='1.0.1',
    license='MIT',
    description='Provide tools to parse and download Mediapart articles as PDF.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Robin Perice',
    author_email='robin.perice@protonmail.com',
    url='https://github.com/r0perice/mediapart-parser',
    download_url='https://github.com/r0perice/mediapart-parser/archive/1.0.1.tar.gz',
    install_requires=[
          'feedparser',
          'beautifulsoup4',
          'requests',
      ],

)