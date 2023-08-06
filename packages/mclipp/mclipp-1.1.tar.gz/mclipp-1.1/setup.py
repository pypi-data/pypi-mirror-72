from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='mclipp',
      version='1.1',
      description='Creating files with custom file size',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['mclipp'],
      author_email='portalproct@gmail.com',
      zip_safe=False)
