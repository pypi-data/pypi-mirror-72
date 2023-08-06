from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'typekev_mlnd_probability', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='typekev_mlnd_probability',
      version='1.1',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['typekev_mlnd_probability'],
      author='Kevin Gonzalez',
      author_email='typekev@gmail.com',
      zip_safe=False)
