from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='stat_probability',
      version='0.2',
      description='Gaussian and Normal distributions.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['stat_probability'],
      author = 'Aniket Hande',
      author_email = 'anikethande779@gmail.com',
      zip_safe=False)
